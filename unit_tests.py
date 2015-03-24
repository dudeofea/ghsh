#!/usr/bin/python
import unittest
from knowledge_net import *

def KNet_equal(test, a, b):
	if len(a.nodes) != len(b.nodes):
		print "Node Length Mismatch"
		return False
	for i in xrange(0, len(a.nodes)):
		if not a.nodes[i] == b.nodes[i]:
			print "Node:"
			print a.nodes[i]
			print "Does not equal:"
			print b.nodes[i]

class SentenceParseTests(unittest.TestCase):
	def test_sent1(self):
		sentence = "he likes him"
		#build answer
		a = KNet()
		a.add_link([a.r('likes'), a.r('he'), a.r('him')])
		#print a
		#parse sentence
		b = KNet()
		b.parse(sentence)
		#print a
		#print b
		KNet_equal(self, a, b)
	def test_sent2(self):
		sentence = "dogs are animals"
		#build answer
		a = KNet()
		a.add_link([a.r('are'), a.r('dogs'), a.r('animals')])
		#parse sentence
		b = KNet()
		b.parse(sentence)
		KNet_equal(self, a, b)
	def test_sent3(self):
		sentence = "good dogs run"
		#build answer
		a = KNet()
		tmp = a.add_link([a.r('good'), a.r('dogs')])
		a.add_link([a.r('run'), tmp])
		#parse sentence
		b = KNet()
		b.parse(sentence)
		print a
		print b
		#KNet_equal(self, a, b)
	def test_sent4(self):
		sentence = "dogs are animals with fur"
		#build answer
		a = KNet()
		tmp = a.add_link([a.r('with'), a.r('animals'), a.r('fur')])
		a.add_link([a.r('are'), a.r('dogs'), tmp])
		#parse sentence
		b = KNet()
		b.parse(sentence)
		#print a
		#print b
		#KNet_equal(self, a, b)

if __name__ == '__main__':
	unittest.main()