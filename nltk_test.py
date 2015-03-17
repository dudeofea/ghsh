#!/usr/bin/python
import nltk
from CFGChartParser import CFGChartParser

sentence = "he likes the girl who wore the green dress"
print sentence
# tag sentence
tagged = nltk.pos_tag(sentence.split())
print tagged
# chunk tags together

parser = CFGChartParser()
for tree in parser.parse(tagged):
	print(tree)
	tree.draw()