# -*- coding: utf-8 -*-
import sys
import os
from natto import MeCab

aozora_data = "./aozora_data"

#convert and split text files in the ./aozora_data
def convert_all(aozora_data):
    for i in os.listdir(aozora_data):
        dir = aozora_data + "/" + i
        dir_utf = dir + "/utf/"
        dir_clean = dir + "/clean/"
        if not os.path.exists(dir_clean):
            try:
                os.makedirs(dir_clean)
                print("make: "+ dir_clean)
            except OSError as e:
                print(e)
        for j in os.listdir(dir_utf):
            dir_utf = dir_utf + j
            convert(dir_utf)


#convert the .txt (delete foreword & afterword)
def convert(download_text):
    binarydata = open(download_text, 'rb').read()
    text = binarydata.decode('shift_jis')

    text = re.split(r'\-{5,}', text)[2]
    text = re.split(r'底本：', text)[0]
    text = re.sub(r'《.+?》', '', text)
    text = re.sub(r'［＃.+?］', '', text)
    text = re.sub(r'\u3000', '', text)
    text = re.sub(r'\r\n', '', text)
    text = text.strip()
    return text
