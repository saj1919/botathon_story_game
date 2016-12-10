import nltk
import re


class YodaConvertor:
    """
    Rule based language converter from English to Yoddish.
    """
    def __init__(self):
        self.question_words = set(['where', 'who', 'when', 'what', 'What', 'why', 'whose', 'which', 'how', '?'])
        self.negative_words = set(['neither', 'never', 'no', 'nobody', 'none', 'nor', 'nothing', 'nowhere', 'not'])
        self.word_replacements = {"can't": "can not", "won't": "will not", "shan't": "shall not",
                                  "ain't": "am not"}
        self.pattern_replacements = {"'m": " am", "'re": " are", "'ve": " have", "'d": " had",
                                     "'ll": " will", "n't": " not"}
        self.special_char = set(['.', '?', '!', 'a', 'an'])
        self.agg_words = set(['should', 'must'])
	self.averbs = set(['is', 'are', 'did', 'have', 'can', 'could', 'will', 'do', 'has', 'had', 
			   'would', 'could', 'may', 'might', 'shall', 'should'])

    def clean_text(self, text):
        for word, replacement in self.word_replacements.iteritems():
            text = re.sub(word, replacement, text)
        for pattern, replacement in self.pattern_replacements.iteritems():
            text = re.sub(pattern, replacement, text)
        return text

    def tokenize_text(self, text):
        text_arr = nltk.word_tokenize(text)
        text_arr = [word.strip() for word in text_arr if word not in self.special_char]
        return text_arr

    def pos_tag_text(self, text_arr):
        return nltk.pos_tag(text_arr)

    def split_sentence(self, text_pos):
        split_pos = -1
        for id_pos, pos_tuple in enumerate(text_pos):
            word, pos = pos_tuple
            if "CC" == pos:
                prev_len = id_pos
                next_len = len(text_pos) - id_pos
		if prev_len >= 3 and next_len >= 3 and "NN" not in text_pos[id_pos-1][1] \
                        and "NN" not in text_pos[id_pos+1][1]:
                    split_pos = id_pos
                    break
        return split_pos

    def detect_question(self, text_arr):
        is_question = False
        word = text_arr[0]
        if word.lower() in self.question_words or word.lower() in self.averbs:
            is_question = True
        return is_question

    def find_first_verb(self, text_pos):
        verb_location = -1
        for vid, vtuple in enumerate(text_pos):
            word, pos = vtuple
            if "VB" in pos or "MD" == pos:
                verb_location = vid
                break
        if verb_location >= 6:
            verb_location = -1
        return verb_location

    def find_first_negation(self, text_arr):
        neg_location = -1
        for wid, word in enumerate(text_arr):
            if word.lower() in self.negative_words:
                neg_location = wid
                break
        if neg_location >= 4:
            neg_location = -1
        return neg_location

    def get_simple_yoda_text(self, text_arr, verb_location, is_question):
        new_text = " ".join(text_arr[verb_location+1:]) + ", " + " ".join(text_arr[: verb_location+1])
        if is_question:
            new_text += "?"
        elif text_arr[verb_location] in self.agg_words:
            new_text += "!"
        else:
            new_text += "."
        new_text = new_text[0].upper() + new_text[1:]
        return new_text

    def get_negation_yoda_text(self, text_arr, neg_location):
        new_text = " ".join(text_arr[neg_location+2:]) + ", " + " ".join(text_arr[:neg_location]) + " " + \
                   text_arr[neg_location+1] + " " + text_arr[neg_location].lower() + "!"
        new_text = new_text[0].upper() + new_text[1:]
        return new_text

    def convert_sentence(self, text, text_arr, pos_text_arr):
	if len(text_arr) < 3:
	    return text
        is_question = self.detect_question(text_arr)
        verb_location = self.find_first_verb(pos_text_arr)
        neg_location = self.find_first_negation(text_arr)

        new_text = text
        if neg_location == -1 and verb_location != -1:
            new_text = self.get_simple_yoda_text(text_arr, verb_location, is_question)
        elif neg_location != -1:
            new_text = self.get_negation_yoda_text(text_arr, neg_location)

        return new_text

    def convert_text(self, text):
        clean_text = self.clean_text(text)
        text_arr = self.tokenize_text(clean_text)
        pos_text_arr = self.pos_tag_text(text_arr)
        print pos_text_arr

        split_pos = self.split_sentence(pos_text_arr)
        if split_pos == -1:
            new_text = self.convert_sentence(text, text_arr, pos_text_arr)
        else:
            new_text1 = self.convert_sentence(text, text_arr[:split_pos], pos_text_arr[:split_pos])
            new_text2 = self.convert_sentence(text, text_arr[split_pos+1:], pos_text_arr[split_pos+1:])
            new_text = new_text1[:-1] + " " + text_arr[split_pos] + " " + new_text2
	return new_text
