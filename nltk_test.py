#!/usr/bin/python
import nltk
from CFGChartParser import CFGChartParser
from brute_tagger import brute_tagger
from knowledge_net import *

sentence = "crabs walk sideways"
print sentence

tagger = brute_tagger('tags.pkl', True)
chunker = CFGChartParser()
tagger.add_tag('walk', ['VBP'])
#print tagger.tag_list
net = KNet()

for t in tagger.tag(sentence.split()):		# get all tag combinations
	print t
	for tree in chunker.parse(t):			# get all chunk combinations
		#print(tree)
		tree.draw()
		net.parse(tree)

tagger.save_tags('tags.pkl')