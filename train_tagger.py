#!/usr/bin/python
import nltk
from brute_tagger import brute_tagger

count = 0
with open('words_en.txt', 'r') as myfile:
	tagger = brute_tagger()
	for w in myfile.readlines():
		word = w.replace('\n','')
		tagger.add_tag(word, [nltk.pos_tag([word])[0][1]])
	tagger.save_tags('tags.pkl')