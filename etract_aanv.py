import nltk
from nltk import *
from nltk.corpus import stopwords
import sys
stop = stopwords.words('english')
f = open(sys.argv[1],"r")
w = open(sys.argv[2],"w")
for i,line in enumerate(f):
	print i,"\r",
	text = word_tokenize(line)
	tags = nltk.pos_tag(text)
	ans = [[],[],[],[]]
	for tag in tags:
		if tag[0] in stop:
			continue
		if "RB" in tag[1][:2]:
			ans[0].append(tag[0])
		elif "JJ" in tag[1][:2]:
			ans[1].append(tag[0])
		if "NN" in tag[1][:2]:
			ans[2].append(tag[0])
		if "VB" in tag[1][:2]:
			ans[3].append(tag[0])
	w.write(str(ans)+"\n")
w.close()
