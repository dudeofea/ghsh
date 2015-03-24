from nltk.tree import Tree
from nltk import CFG, help
from copy import copy

class CFGChartParser(object):
	grammar = ""

	def __init__(self):
		self.grammar = CFG.fromstring("""
			S -> NP VP
			PP -> P NP
			VP -> V NP | VP PP | V
			NP -> Det N | Det ADJ N | Det N PP | ADJ NP | NP S | N | 'WP'
			Det -> 'DT' | 'PRP$'
			N -> 'NN' | 'PRP' | 'NNS'
			V -> 'VBD' | 'VBP' | 'VBZ' | 'RB' 
			P -> 'IN'
			ADJ -> 'JJ'
		""")
	
	def parse(self, words):
		s = None
		unmerged = []
		#match the words themselves
		for word in words:
			matched = False
			for p in self.grammar.productions():
				for r in p.rhs():
					if word[1] == r:
						matched = True
						unmerged.append(Tree(p.lhs(), [word[0]]))
			#if you can't match the word
			if not matched:
				print "Couldn't find tag for", "'"+word[0]+"'", "("+word[1]+")"
				print help.upenn_tagset(word[1])
		#match the rest
		unmerged = self.find_all_trees(unmerged)
		#remove all sentences that aren't sentences
		unmerged = [u for u in unmerged if str(u.label()) == 'S' and self.leaf_count(u) == len(words)]
		return unmerged

	def leaf_count(self, tree):
		if not hasattr(tree, "__iter__"):
			return 1
		s = 0
		for t in tree:
			s += self.leaf_count(t)
		return s

	def find_all_trees(self, tree):
		labels = [u.label() for u in tree]
		merges = self.find_rhs_matches(labels)
		trees = []
		for merge in merges:
			tmp_tree = copy(tree)
			tmp_tree = self.perform_merge(tmp_tree, merge)
			tmp_tree = self.find_all_trees(tmp_tree)
			for t in tmp_tree:
				if t not in trees:
					trees.append(t)
		if len(trees) == 0:
			trees = tree #we're done
		return trees

	def perform_merge(self, tree, merge):
		p = self.grammar.productions()[merge[0]]
		rhs = p.rhs()
		i = merge[1]
		u = tree[i:i+len(rhs)]
		if len(rhs) == 1:
			t = Tree(p.lhs(), [u[0][0]])
		else:
			t = Tree(p.lhs(), u)
		del tree[i:i+len(rhs)]
		tree.insert(i, t)
		return tree

	def find_rhs_matches(self, labels):
		r = []
		prod = self.grammar.productions()
		for i in xrange(0, len(prod)):
			p = prod[i]
			rhs = p.rhs()
			matches = self.find_rhs_match(rhs, labels)
			for match in matches:
				r.append([i, match])
		return r
	#find a match with right hand side requesites within labels
	def find_rhs_match(self, rhs, labels):
		ans = []
		rhs_i = 0
		for i in xrange(0, len(labels)):
			if labels[i] == rhs[rhs_i]:
				rhs_i += 1
				if rhs_i >= len(rhs): #if matched the whole thing
					ans.append(i - rhs_i + 1)
					rhs_i = 0
			else:
				rhs_i = 0
		return ans