from nltk.tree import Tree
from nltk import CFG

class CFGChartParser(object):
	grammar = ""

	def __init__(self):
		self.grammar = CFG.fromstring("""
			S -> NP VP
			PP -> P NP
			VP -> V NP | VP PP
			NP -> Det N | Det N PP | N
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
		#TODO: find a way to print every combination of single root trees
		labels = [u.label() for u in unmerged]
		m = self.run_pass(labels)
		while len(m) > 0:
			# perform merges
			offset = 0
			for match in m:
				p = self.grammar.productions()[match[0]]
				rhs = p.rhs()
				i = match[1] - offset
				offset += len(rhs) - 1
				u = unmerged[i:i+len(rhs)]
				if len(rhs) == 1:
					t = Tree(p.lhs(), [u[0][0]])
				else:
					t = Tree(p.lhs(), u)
				del unmerged[i:i+len(rhs)]
				unmerged.insert(i, t)
				a = [str(u) for u in unmerged]
			print a
			labels = [u.label() for u in unmerged]
			m = self.run_pass(labels)
		return unmerged

	def run_pass(self, labels):
		r = []
		prod = self.grammar.productions()
		for i in xrange(0, len(prod)):
			p = prod[i]
			rhs = p.rhs()
			matches = self.find_rhs_match(rhs, labels)
			for match in matches:
				print "Match:", p.lhs(), "->", p.rhs(), match
				r.append([i, match])
			if len(matches) > 0:
				break
		return r

	def find_rhs_match(self, rhs, labels):
		ans = []
		rhs_i = 0
		for i in xrange(0, len(labels)):
			if labels[i] == rhs[rhs_i]:
				rhs_i += 1
				if rhs_i >= len(rhs):
					ans.append(i - rhs_i + 1)
					rhs_i = 0
			else:
				rhs_i = 0
		return ans