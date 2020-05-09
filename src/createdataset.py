import re
import os
import pandas as pd
from tqdm import tqdm


puncts = [',', '.', '"', ':', ')', '(', '-', '!', '?', '|', ';', "'", '$', '&', '/', '[', ']', '>', '%', '=', '#', '*', '+', '\\', '•',  '~', '@', '£',
 '·', '_', '{', '}', '©', '^', '®', '`',  '<', '→', '°', '€', '™', '›',  '♥', '←', '×', '§', '″', '′', 'Â', '█', '½', 'à', '…', '\n', '\xa0', '\t',
 '“', '★', '”', '–', '●', 'â', '►', '−', '¢', '²', '¬', '░', '¶', '↑', '±', '¿', '▾', '═', '¦', '║', '―', '¥', '▓', '—', '‹', '─', '\u3000', '\u202f',
 '▒', '：', '¼', '⊕', '▼', '▪', '†', '■', '’', '▀', '¨', '▄', '♫', '☆', 'é', '¯', '♦', '¤', '▲', 'è', '¸', '¾', 'Ã', '⋅', '‘', '∞', '«',
 '∙', '）', '↓', '、', '│', '（', '»', '，', '♪', '╩', '╚', '³', '・', '╦', '╣', '╔', '╗', '▬', '❤', 'ï', 'Ø', '¹', '≤', '‡', '√', ]


def create_dataset(path:str):
    categories = os.listdir(path)
    data=[]
    sequence=''
    for category in categories:
        new_path = f'{path}/{category}'
        texts = os.listdir(new_path)
        for text in tqdm(texts):
            with open(f'{new_path}/{text}', encoding='UTF-8') as f:
                count=0
                for x in f:
                    q=re.findall('\С. \d+', x)
                    q1=re.findall('\с. \d+', x)
                    q2=re.findall('\(\d+', x)
                    if len(q2)!=0:
                        print(q2)
                    if (len(x)>30) & (len(q)==0) & (len(q1)==0) & (len(q2)==0):
                        if len(sequence)<1500:
                            x = re.sub('\n', '', x)
                            x = re.sub('\*', '', x)
                            x = re.sub('\[\d+\]', '', x)
                            x = re.sub('\¬ ', '', x)
                            x = re.sub('\t', ' ', x)
                            x = re.sub('\■', '', x)
                            x = re.sub('\(\w+\.\)', '', x)
                            #x = clean_text(x)
                            #x = clean_numbers(x)
                            sequence+=x
                        else:
                            count+=1
                            if count>3:
                                data.append({'text': sequence,
                                             'category': category})
                            sequence=''
                data = data[:-5]
    text_df = pd.DataFrame(data)
    return text_df                


if __name__=='__main__':
    path = r'D:\NLP\TestDataset'
    text_df = create_dataset(path)
    text_df.to_csv(f'{path}/text_df.csv', index=False)
