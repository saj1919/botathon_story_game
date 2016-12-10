from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
import re
import random

stopwords = stopwords.words('english')


class rrhyme:

    def __init__(self, input_file):
        self.text_lastword_dict = self.tokenize_book(input_file)
        self.done_text_set = set()

    def tokenize_book(self, file_path):
        fr = open(file_path, 'r')
        text = fr.read()
        fr.close()

        text_lastword_dict = {}

        text = re.sub("([\(\[]).*?([\)\]])", " ", text)
        text = re.sub("\s+", ' ', text)
        text = re.sub(r'[^\x00-\x7F]+', ' ', text)
        text = re.sub("\s+", ' ', text)

        text_arr = sent_tokenize(text.lower())
        for x in text_arr:
            x = re.sub("illustration", " ", x)
            x = re.sub("'", "", x)
            x = re.sub("-", "", x)
            x = re.sub("[^A-Za-z0-9]", " ", x)
            x = re.sub("\s+", ' ', x)
            x = x.strip()
            if x != "" and 5 <= len(x.split()) <= 10:
                x_words = x.split()
                x_words_new = []
                for w in x_words:
                    w = w.strip()
                    if w not in stopwords:
                        x_words_new.append(w)
                for w in x_words_new:
                    if w not in text_lastword_dict:
                        text_lastword_dict[w] = [x]
                    else:
                        text_lastword_dict[w].append(x)
        return text_lastword_dict

    def get_rhym_text(self, input_text):
        input_text = re.sub(r'[^\x00-\x7F]+', ' ', input_text.lower())
        input_text = re.sub("\s+", ' ', input_text)
        input_text = re.sub("[^A-Za-z0-9]", " ", input_text)
        input_text = re.sub("\s+", ' ', input_text)

        input_text_arr = []
        for w in input_text.split():
            w = w.strip()
            if w not in stopwords:
                input_text_arr.append(w)
        if len(input_text_arr) > 0:
            random.shuffle(input_text_arr)
            last_word = input_text_arr[0]
        else:
            last_word = input_text.split()[-1].strip()

        bot_text_arr = self.text_lastword_dict[last_word]
        random.shuffle(bot_text_arr)
        return bot_text_arr[0]


if __name__ == '__main__':
    # input_file = '../../data/harry_potter_books_1_4.txt'
    input_file = "/home/haptik/Documents/poems/all_poems.txt"
    obj = rhyme(input_file)
    while True:
        input_text = raw_input("YOU : ")
        print "BOT : ", obj.get_rhym_text(input_text)

