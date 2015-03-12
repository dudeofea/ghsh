#!/usr/bin/python
import nltk
from CFGChartParser import CFGChartParser

sentence = "I shot an elephant in my pyjamas"
print sentence
# tag sentence
tagged = nltk.pos_tag(sentence.split())
#print tagged
# chunk tags together

parser = CFGChartParser()
for tree in parser.parse(tagged):
	print(tree)
#	tree.draw()