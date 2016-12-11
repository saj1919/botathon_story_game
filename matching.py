import nltk
from nltk import *
from nltk.corpus import stopwords
import sys,ast
class StoryBot:
	def __init__(self):
		self.stop = stopwords.words('english')
		self.msgs = open("mixed_books_per_sentence.tsv","r").readlines()
		self.tags = []
		for line in open("tagged.txt","r"):
			try:
				x = ast.literal_eval(line.strip())
				self.tags.append(set(x[0]+x[1]+x[2]+x[3]))
			except:
				print line
		self.inp = ""
	def get_reco(self,curr):
		print "User:",
		self.inp = self.inp + curr 
		self.inp = " ".join(self.inp.split()[-40:])
		print "Bot:",
		res = []
		text = word_tokenize(self.inp)
		tags_inp = nltk.pos_tag(text)
		tmp = []
		for tag in tags_inp:
			if tag[0] in self.stop:
				continue
			if "RB" in tag[1][:2]:
				tmp.append(tag[0])
			elif "JJ" in tag[1][:2]:
				tmp.append(tag[0])
			elif "NN" in tag[1][:2]:
				tmp.append(tag[0])
			elif "VB" in tag[1][:2]:
				tmp.append(tag[0])
		tmp = set(tmp)
		for i,tup in enumerate(zip(self.tags, self.msgs)):
			try:
				res.append((tup[0] & tmp, 0-len(self.msgs[i+1].split()), 0-len(tup[1].split()), i))
			except:
				continue
		print self.msgs[max(res)[3]]
		print self.msgs[max(res)[3]+1]
		self.inp += self.msgs[max(res)[3]+1]
		return self.msgs[max(res)[3]].strip()+self.msgs[max(res)[3]+1].strip()
