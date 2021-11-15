import django
import os
import re

import api
from django.conf import settings

def remove_punctuation(string):
    words = re.findall('[^!\n \r\u200c،"؛.,:-؟]+', string)
    return words


def get_learning_datas():
    learning_words = []
    path = os.path.join(settings.BASE_DIR, 'api/learning_datas')
    files = os.listdir(path)
    for i in files:
        with open(os.path.join(path, i), 'r', encoding="utf-8") as reader:
            file_content = reader.read()
            learning_words.extend(remove_punctuation(file_content))
    return learning_words

def text_processing(word, learning_words):
    if word.endswith('ان') or word.endswith('ها'):
        if word[0:-2:1] in learning_words:
            word = word[0:-2:1]
    if word.endswith('ی'):
        if word[0:-1:1] in learning_words:
            word = word[0:-1:1]
    if word == 'می' or word == 'ها':
        word = None
    if word == 'نمی' :
        word = None
    return word
