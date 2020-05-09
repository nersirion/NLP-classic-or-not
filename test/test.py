
import re

import os
import pytest
import src.utils as utils



test_str = 'xfdf fsdaf sa dfsd fsd d asadf sadf lkdfl ldfk alsd ldakl'
def test_split_str():
    result = utils.split_str(test_str)
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

def test_concat_data():
    test_str = ["join", "party", "please"]
    concat_data = utils.DataAggregator()
    for x in test_str: result=concat_data(x)
    result = concat_data.sequence.strip()
    assert result == "join party please"

true_result = [{"text": "Текст для тестов."},
              {"text": "Один, два, три."},
              {"text": "Четыре, восемь. как-то"},
              {"text": "так и никак"},
              {"text": "иначе"}]

def test_read_file():
    path = r"C:\Users\Nersirion\NLP_classis_or_not\test\files_for_test\test_file.txt"
    result = utils.read_file(path)
    assert result == true_result 

def test_FilesList():
    path = r"C:\Users\Nersirion\NLP_classis_or_not\test"
    fl = utils.FileReader(path)
    for r in fl: pass
    result = fl.data_agg.data
    assert result == true_result 

