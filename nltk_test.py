#!/usr/bin/python
import nltk
from CFGChartParser import CFGChartParser
sentence = "I shot an elephant in my pyjamas"
#print sentence
# tag sentence
tagged = nltk.pos_tag(sentence.split())
#print tagged
# chunk tags together
grammar = """
	S:
		{<NP><VP>}
    NP:
        {<DT>?<JJ>*<NN>}
        {<DT><NN><PP>}
        {<PRP\$><JJ>*<NNS>}
        {<PRP>}
    PP:
    	{<IN><NP>}
    VP:
    	{<VBD><NP>}
    	{<VP><PP>}
"""
#parser = nltk.RegexpParser(grammar)
parser = CFGChartParser()
for tree in parser.parse(tagged):
	print(tree)
	tree.draw()