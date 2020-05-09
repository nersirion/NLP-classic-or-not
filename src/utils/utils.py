import re


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

def find_comment(x:str) -> list:
    pattern = '\С. \d+|\с. \d+|\(\d+'
    return re.findall(pattern, x)

def find_values_text(x:str) -> bool:
    comment = find_comment(x)
    if len(x) > 30 and not comment:
        return True
    return False

def create_data(x:str) -> list:
    result = split_str(x)
    data = [{'text': ' '.join(tokens)} for tokens in result]
    return data

def check_len_tokens(x:str) -> bool:
    tokens = x.split()
    return len(tokens)>NUMBER

def recursion_concat(x:str) -> str:
    new_str = x
    if 
