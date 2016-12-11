import random
import re
import string
import traceback
import cherrypy
from yoda_util import YodaConvertor
from rhyme_story import rhyme
from romantic_poems import rrhyme
from matching import StoryBot

class StringGenerator(object):

    def __init__(self, poem_input_file, rpoem_input_file):
	self.story_obj = StoryBot()
	self.yc_obj = YodaConvertor()
	self.poem_obj = rhyme(poem_input_file)
	self.rpoem_obj = rhyme(rpoem_input_file)
	self.rrpoem_obj = rrhyme(rpoem_input_file)
	self.global_context = "help"
	self.global_prev_context = "help"
	self.prev_romatic_bot_reply = ""

    @cherrypy.expose
    def main_api(self, my_text="SOMETHING", method="get", _="none"):
	my_msg = my_text.split('?_=')[0]
	if my_msg == "help" or my_msg == "quit" or my_msg == "exit" or my_msg == "end":
	    self.prev_romatic_bot_reply = ""
            self.global_prev_context = self.global_context
            self.global_context = "help"
        elif my_msg == "yoda":
	    self.prev_romatic_bot_reply = ""
            self.global_prev_context = self.global_context
            self.global_context = "yoda"
	elif my_msg == "story":
            self.prev_romatic_bot_reply = ""
            self.global_prev_context = self.global_context
            self.global_context = "story"
        elif my_msg == "poem":
	    self.prev_romatic_bot_reply = ""
            self.global_prev_context = self.global_context
            self.global_context = "poem"
	elif my_msg == "romantic":
            self.global_prev_context = self.global_context
            self.global_context = "romantic"
        else:
            self.global_prev_context = self.global_context

	if self.global_context == "help":
            return "Type 'poem' to play poem Creation game. Type 'romantic' to play bf-gf game. Type 'yoda' to get yodish echo. Type 'help', 'quit', 'exit' for getting help."
	elif self.global_context == "yoda":
            if self.global_context != self.global_prev_context:
            	return "Type Something and get Yoda-Echo !!"
	    else:
	    	return self.yoda_test(my_msg)
    	elif self.global_context == "poem":
            if self.global_context != self.global_prev_context:
                return "Type Something and generate Poems !!"
     	    else:
		return self.poem_test(my_msg)
	elif self.global_context == "story":
            if self.global_context != self.global_prev_context:
                return "Type your story lines and get context-aware story !!"
            else:
                return self.story_test(my_msg)
	elif self.global_context == "romantic":
            if self.global_context != self.global_prev_context:
                return "Type Something and generate romatic poems game !! Rule is to include proper word (no stopword) from previous msg."
            else:
                return self.rpoem_test(my_msg)

    @cherrypy.expose
    def rpoem_test(self, my_text="SOMETHING"):
	try:
	    input_text = re.sub(r'[^\x00-\x7F]+', ' ', my_text.lower())
            input_text = re.sub("\s+", ' ', input_text)
            input_text = re.sub("[^A-Za-z0-9]", " ", input_text)
            input_text = re.sub("\s+", ' ', input_text)
	    user_word_arr = input_text.split()
	    if self.prev_romatic_bot_reply == "":
            	self.my_text = self.rrpoem_obj.get_rhym_text(my_text)
		self.prev_romatic_bot_reply = self.my_text
            	return self.my_text
	    else:
		bot_word_arr = self.prev_romatic_bot_reply.split()
		if set(user_word_arr) & set(bot_word_arr):
		    self.my_text = self.rrpoem_obj.get_rhym_text(my_text)
		    self.prev_romatic_bot_reply = self.my_text
                    return self.my_text
		else:
		    self.global_context = "help"
	            self.global_prev_context = "help"
		    return "You have not included any proper word from previous msg. YOU LOST !! Type 'exit', 'help' for main menu."
	except Exception as e:
            traceback.print_exc()
	    self.prev_romatic_bot_reply = self.yoda_test(my_text)
	    return self.prev_romatic_bot_reply

    @cherrypy.expose
    def poem_test(self, my_text="SOMETHING"):
	try:
            self.my_text = self.poem_obj.get_rhym_text(my_text)
            return self.my_text
        except Exception as e:
            return self.yoda_test(my_text)

    @cherrypy.expose
    def yoda_test(self, my_text="SOMETHING"):
        self.my_text = self.yc_obj.convert_text(my_text)
	return self.my_text

    @cherrypy.expose
    def story_test(self, my_text="SOMETHING"):
        self.my_text = self.story_obj.get_reco(my_text)
        return self.my_text


if __name__ == '__main__':
    poem_input_file = "/home/ubuntu/botathon/data/all_poems.txt"
    rpoem_input_file = "/home/ubuntu/botathon/data/romantic_poems.txt"
    cherrypy.config.update({'server.socket_host': '0.0.0.0'})
    cherrypy.quickstart(StringGenerator(poem_input_file, rpoem_input_file))
