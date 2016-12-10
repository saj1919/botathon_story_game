from nltk.tokenize import sent_tokenize
import re
import operator
from rhymes import word_similarity
import random


class rhyme:

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
                lastword = x.split()[-1].strip()
                if lastword not in text_lastword_dict:
                    text_lastword_dict[lastword] = [x]
                else:
                    text_lastword_dict[lastword].append(x)
        return text_lastword_dict

    def get_rhym_text(self, input_text):
        input_text = re.sub(r'[^\x00-\x7F]+', ' ', input_text.lower())
        input_text = re.sub("\s+", ' ', input_text)
        input_text = re.sub("[^A-Za-z0-9]", " ", input_text)
        input_text = re.sub("\s+", ' ', input_text)

        last_word = input_text.split()[-1].strip()
        rhym_score = {}
        wcount = 0

        for w, s in self.text_lastword_dict.items():
            if w != last_word and len(w) > 3:
                rhym_score[w] = word_similarity(w, last_word)
            wcount += 1

        rhym_score = sorted(rhym_score.items(), key=operator.itemgetter(1), reverse=True)
        highest_score_words = []
        max_score = rhym_score[0][1]
        if max_score > 0:
            for w, s in rhym_score:
                if s >= max_score:
                    highest_score_words.append(w)
            random.shuffle(highest_score_words)
            bot_text = self.text_lastword_dict[highest_score_words[0]]
        else:
            random.shuffle(rhym_score)
            bot_text = self.text_lastword_dict[rhym_score[0][0]]
        random.shuffle(bot_text)
        return bot_text[0]


if __name__ == '__main__':
    # input_file = '../../data/harry_potter_books_1_4.txt'
    input_file = "/home/haptik/Documents/poems/all_poems.txt"
    obj = rhyme(input_file)
    while True:
        input_text = raw_input("YOU : ")
        print "BOT : ", obj.get_rhym_text(input_text)
