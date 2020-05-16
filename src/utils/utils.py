import re
import os
import json
import pandas as pd
import config


def split_str(x: str, token_split: int = config.TOKEN_SPLIT) -> list:
    tokens = x.split()
    split_range = range(0, len(tokens), token_split)
    result = [tokens[i : i + token_split] for i in split_range]
    return result


def clean_text(text: str) -> str:
    text = str(text).lower()
    text = re.sub("[^а-я0-9\s]", "", text)
    text = clean_numbers(text)
    return text


def clean_numbers(x: str) -> str:
    x = re.sub("[0-9]{5,}", "#####", x)
    x = re.sub("[0-9]{4}", "####", x)
    x = re.sub("[0-9]{3}", "###", x)
    x = re.sub("[0-9]{2}", "##", x)
    return x


class DataAggregator:
    def __init__(self):
        self.sequence = ""
        self.data = []

    def __call__(self, x, category):
        self.sequence += x + " "
        if check_len_tokens(self.sequence):
            self.data += create_data(self.sequence, category)
            self.reset_sequence()

    def reset_sequence(self):
        self.sequence = ""


def find_comment(x: str) -> list:
    pattern = "\С. \d+|\с. \d+|\(\d+"
    return re.findall(pattern, x)


def find_values_text(x: str) -> bool:
    comment = find_comment(x)
    if len(x) > config.MIN_LEN_FOR_STR and not comment:
        return True
    return False


def create_data(x: str, category: str) -> list:
    result = split_str(x)
    data = [{"text": " ".join(tokens), "category": category} for tokens in result]
    return data


def check_len_tokens(x: str) -> bool:
    tokens = x.split()
    return len(tokens) >= config.TOKEN_SPLIT


def check_str_ready(x: str) -> bool:
    check = find_values_text(x) and check_len_tokens(x)
    return check


class FileReader(DataAggregator):
    def __init__(self, path: str):
        super().__init__()
        self.folders = [
            folder
            for folder in os.listdir(path)
            if os.path.isdir(f"{path}/{folder}") and not folder.startswith(("__", "."))
        ]
        self.path = path

    def __len__(self):
        return len(self.folders)

    def __getitem__(self, ind: int):
        category = self.folders[ind]
        file_path = f"{self.path}/{category}"
        [
            self.read_file(f"{file_path}/{file}", category)
            for file in os.listdir(file_path)
            if file.endswith(".txt")
        ]
        return category

    def aggregate_data(self, file, category) -> list:
        for x in file:
            if find_values_text(x):
                x = clean_text(x)
                self(x, category)

    def read_file(self, file_path: str, category: str):
        with open(file_path, encoding="UTF-8") as f:
            self.aggregate_data(f, category)


def final_check(text: str, min_tokens: int = config.MIN_TOKENS) -> bool:
    text = text.split()
    return len(text) > min_tokens


def cut_short_str(data: list) -> list:
    data = [d for d in data if final_check(d["text"])]
    return data


def create_dataset(path: str = config.PATH):
    fr = FileReader(path)
    for folder in fr:
        print(f"{folder}...")
    save_path = f"{path}/dataset.json"
    fr.data = cut_short_str(fr.data)
    with open(save_path, "w") as json_file:
        json.dump(fr.data, json_file)
    print("Done")
