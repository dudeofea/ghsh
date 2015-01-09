from nltk.tree import Tree
from nltk import CFG

class CFGChartParser(object):
	grammar = ""

	def __init__(self):
		self.grammar = CFG.fromstring("""
			S -> NP VP
			PP -> P NP
			NP -> Det N | Det N PP | N
			VP -> V NP | VP PP
			Det -> 'DT' | 'PRP$'
			N -> 'NN' | 'PRP' | 'NNS'
			V -> 'VBD'
			P -> 'IN'
		""")
	
	def parse(self, words):
		s = None
		unmerged = []
		#match the words themselves
		for word in words:
			for p in self.grammar.productions():
				for r in p.rhs():
					if word[1] == r:
						unmerged.append(Tree(p.lhs(), [word[0]]))
		#match the rest
		done = False
		while not done:
			done = True
			for p in self.grammar.productions():
				rhs = p.rhs()
				i = self.find_rhs_match(rhs, [u.label() for u in unmerged])
				if i >= 0:
					#print "Match:", rhs
					u = unmerged[i:i+len(rhs)]
					if len(rhs) == 1:
						t = Tree(p.lhs(), [u[0][0]])
					else:	
						t = Tree(p.lhs(), u)
					del unmerged[i:i+len(rhs)]
					unmerged.insert(i, t)
					a = [str(u) for u in unmerged]
					print a
					done = False
					break
		return unmerged

	def find_rhs_match(self, rhs, labels):
		#print rhs, labels
		rhs_i = 0
		for i in xrange(0, len(labels)):
			if labels[i] == rhs[rhs_i]:
				rhs_i += 1
				if rhs_i >= len(rhs):
					return i - rhs_i + 1
			else:
				rhs_i = 0
		return -1