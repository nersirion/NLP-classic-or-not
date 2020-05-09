import re
import os


NUMBER = 3
def split_str(x:str, token_split:int=3) -> list:
    tokens = x.split()
    split_range = range(0, len(tokens), token_split)
    result = [tokens[i:i+token_split] for i in split_range]
    return result

def clean_text(x):
    x = str(x)
    for punct in puncts:
        x = x.replace(punct, f' {punct} ')
    return x

def clean_numbers(x):
    x = re.sub('[0-9]{5,}', '#####', x)
    x = re.sub('[0-9]{4}', '####', x)
    x = re.sub('[0-9]{3}', '###', x)
    x = re.sub('[0-9]{2}', '##', x)
    return x

class DataAggregator:
    sequence = ""
    data = []

    def __call__(self, x):
        self.sequence += x + " "
        if check_len_tokens(self.sequence):
            self.data += create_data(self.sequence)
            self.reset_sequence()
    
    def reset_sequence(self):
        self.sequence = ""

def find_comment(x:str) -> list:
    pattern = '\С. \d+|\с. \d+|\(\d+'
    return re.findall(pattern, x)

def find_values_text(x:str) -> bool:
    comment = find_comment(x)
    if len(x) > 3 and not comment:
        return True
    return False

def create_data(x:str) -> list:
    result = split_str(x)
    data = [{'text': ' '.join(tokens)} for tokens in result]
    return data

def check_len_tokens(x:str) -> bool:
    tokens = x.split()
    return len(tokens)>NUMBER

def check_str_ready(x:str) -> bool:
    check = find_values_text(x) and check_len_tokens(x)
    return check

data_agg = DataAggregator()
def aggregate_data(file) -> list:
    for x in file:
        if find_values_text(x):
            data_agg(x)
    return data_agg.data 


def read_file(file_path:str) -> list:
    with open(file_path, encoding="UTF-8") as f:
        data = aggregate_data(f)
    return data



class FileReader:

    def __init__(self, path:str):
        self.folders = [folder for folder in os.listdir(path)
                        if os.path.isdir(f"{path}/{folder}")
                        and not folder.startswith(("__", "."))]
        self.data_agg = DataAggregator()
        self.path = path

    def __len__(self):
        return len(self.folders)

    def __getitem__(self, ind:int):
        self.category = self.folders[ind]
        file_path = f"{self.path}/{self.category}"
        self.data_agg.data += [read_file(f"{file_path}/{file}") \
                               for file in os.listdir(file_path) \
                               if file.endswith(".txt")]
        




def create_dataset():
    fl = FileReader(config.PATH)
    for folder in fl:
        print(f"Обрабатываются файлы в папке {folder}")
    df = pd.DataFrame(fl.data_agg.data)
    df.to_csv(f"{config.PATH}/dataset.csv", index=False)
    print("Данные обработаны и успешно сохранены")
