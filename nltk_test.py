#!/usr/bin/python
import nltk
from CFGChartParser import CFGChartParser
from knowledge_net import *

k = KNet()
k.add_node(KNode('animal'))
k.add_node(KNode('dog'))
k.add_node(KNode('fur'))
k.add_node(KNode('vertebrates'))
#dogs are animals with fur
k.add_link(0, 1, WithKLink(2))

#animals are vertebrates
k.add_link(3, 0, AreKLink())

#print k
#are dogs vertebrates?
print k.find_is(1, 3)

#sentence = "dogs have legs"
#print sentence
# tag sentence
#tagged = nltk.pos_tag(sentence.split())
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

#parser = CFGChartParser()
#for tree in parser.parse(tagged):
#	print(tree)
#	tree.draw()