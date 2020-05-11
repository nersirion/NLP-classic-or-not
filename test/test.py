
import re

import os
import json
import pytest
import pandas as pd
import src.utils as utils



test_str = 'xfdf fsdaf sa dfsd fsd d asadf sadf lkdfl ldfk alsd ldakl'
def test_split_str():
    result = utils.split_str(test_str, token_split=3)
    assert len(result) == 4

def test_split_str_notchange():
    result = utils.split_str(test_str)
    result_str = ' '.join([' '.join(tokens) for tokens in result])
    assert result_str == test_str


def test_find_comment():
    test_str = 'С. 258 - с. 259 что-то. С.298 это, 1829 средний , с.124 ничего, (1990-2001)'
    result = utils.find_comment(test_str)
    assert result == ['С. 258', 'с. 259', '(1990']

def test_find_values_text():
    test_str = 'С. 258 - с. 259 что-то. С.298 это, 1829 средний , с.124 ничего, (1990-2001)'
    result = utils.find_values_text(test_str)
    assert result == False

def test_create_data():
   result = utils.create_data(test_str)
   assert result == [{'text': 'xfdf fsdaf sa'},
                     {'text': 'dfsd fsd d'},
                     {'text': 'asadf sadf lkdfl'},
                     {'text': 'ldfk alsd ldakl'}]

path = r"C:\Users\Nersirion\NLP_classis_or_not\test"   
def test_concat_data():
    test_str = ["join", "party", "please"]
    file_reader = utils.FileReader(path)
    for x in test_str: file_reader(x)
    result = file_reader.data
    assert result == [{"text": "join party please"}]

true_result = [{"text": "Текст для тестов."},
              {"text": "Один, два, три."},
              {"text": "Четыре, восемь. как-то"},
              {"text": "так и никак"},
              {"text": "иначе"}]

def test_read_file():
    file_path = r"C:\Users\Nersirion\NLP_classis_or_not\test\files_for_test\test_file.txt"
    file_reader = utils.FileReader(path)
    file_reader.read_file(file_path)
    result = file_reader.data
    assert result == true_result 


def test_FilesList():
    fr = utils.FileReader(path)
    for r in fr: pass
    result = fr.data
    assert result == true_result 

def test_create_dataset():
    utils.create_dataset(path)
    json_path = f"{path}/dataset.json"
    with open(json_path) as json_file:
        result = json.load(json_file)
    assert result == true_result
