#!/usr/bin/python
import nltk
from CFGChartParser import CFGChartParser
from brute_tagger import brute_tagger

sentence = "I shot an elephant in my pyjamas"
print sentence

tagger = brute_tagger('tags.pkl')
chunker = CFGChartParser()
#tagger.add_tag('shot', ['VBD'])

for t in tagger.tag(sentence.split()):		# get all tag combinations
	for tree in chunker.parse(t):			# get all chunk combinations
		print(tree)
		tree.draw()

#tagger.save_tags('tags.pkl')