import random
import string

import cherrypy
from yoda_util import YodaConvertor
from rhyme_story import rhyme


class StringGenerator(object):

    def __init__(self, poem_input_file):
	self.yc_obj = YodaConvertor()
	self.poem_obj = rhyme(poem_input_file)
	self.global_context = "help"
	self.global_prev_context = "help"

    @cherrypy.expose
    def main_api(self, my_text="SOMETHING", method="get", _="none"):
	my_msg = my_text.split('?_=')[0]
	if my_msg == "help" or my_msg == "quit" or my_msg == "exit" or my_msg == "end":
            self.global_prev_context = self.global_context
            self.global_context = "help"
        elif my_msg == "yoda":
            self.global_prev_context = self.global_context
            self.global_context = "yoda"
        elif my_msg == "poem":
            self.global_prev_context = self.global_context
            self.global_context = "poem"
        else:
            self.global_prev_context = self.global_context

	if self.global_context == "help":
            return "Type 'poem' to play poem Creation game. Type 'yoda' to get yodish echo. Type 'help', 'quit', 'exit' for getting help."
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

    @cherrypy.expose
    def poem_test(self, my_text="SOMETHING"):
        self.my_text = self.poem_obj.get_rhym_text(my_text)
        return self.my_text

    @cherrypy.expose
    def yoda_test(self, my_text="SOMETHING"):
        self.my_text = self.yc_obj.convert_text(my_text)
	return self.my_text

if __name__ == '__main__':
    poem_input_file = "/home/ubuntu/botathon/data/all_poems.txt"
    cherrypy.config.update({'server.socket_host': '0.0.0.0'})
    cherrypy.quickstart(StringGenerator(poem_input_file))
