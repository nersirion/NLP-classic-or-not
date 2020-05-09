
import re
import os
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
    for x in test_str: result=con_data(x)
    assert result == "join party please"

