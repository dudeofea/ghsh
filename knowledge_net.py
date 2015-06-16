import copy, nltk
from CFGChartParser import CFGChartParser

#find a child with label
def t_find(tree, labels):
	for c in tree:
		if not hasattr(c, 'label'):
			return None
		if str(c.label()) in labels:
			return c
		c2 = t_find(c, labels)
		if c2 != None:
			return c2
	return None
#returns true if tree node matches given form
def t_children_are(tree, child_s):
	for i in xrange(0, len(tree)):
		if str(tree[i].label()) != child_s[i]:
			return False
	return True

class KNet(object):
	"""Net of knowledge composed of nodes linked to each other"""
	def __init__(self):
		self.nodes = []
	def add_node(self, node):
		self.nodes.append(node)
		return len(self.nodes)-1
	def get(self, port):
		#return the thing
		if port.sel_sub < 0:
			return self.nodes[port.index]
		#return a subthing
		return self.nodes[port.sel_sub]
	#creates a new link, all node_l's must exist
	def add_link(self, node_l):
		link_n = node_l[0]
		del node_l[0]
		#make a new instance of a link
		link = copy.deepcopy(self.get(link_n))
		link.links = node_l
		link.ref = link_n
		new_link_i = self.add_node(link)
		# set links in all referred indexes
		length = len(self.nodes)
		subs = []
		for i in node_l:
			if i.index < length and i.index > -1:
				self.nodes[i.index].linked_to.append(new_link_i)
				subs.append({'name': self.nodes[i.index].name, 'index': i.index})
		port = KPort(new_link_i, subs)
		return port
	#find node index by name
	def find(self, name):
		for x in xrange(0, len(self.nodes)):
			if self.nodes[x].name == name:
				return x
		return -1
	#either returns the index or creates a
	#new node and returns it's index
	def r(self, name):
		i = self.find(name)
		if i < 0:
			i = self.add_node(KNode(name))
		port = KPort(i, [])
		return port
	#parses a sentence and ads it to the KNet
	def parse(self, tree):
		#find what is doing what?
		new_net = KNet()
		self._parseNode(tree, new_net)
		print new_net
	#parses a certain gramatical node of a sentence tree
	#returns a KNet representing the sentence
	def _parseNode(self, node, net, net_i=-1):
		#get node type
		ntype = str(node.label())
		for n in node:
			if not hasattr(n, 'label'):
				break
			ntype += ","+str(n.label())
		if ntype == 'S,NP,VP':		#sentence
			#parse noun
			noun = net.add_node(KNode(''))
			self._parseNode(node[0], net, noun)
			#parse verb phrase
			verb = net.add_node(KNode(''))
			net.nodes[verb].links.append(KPort(noun))
			self._parseNode(node[1], net, verb)
		elif ntype == 'VP,VP,PP':	#modified verb phrase
			#parse verb phrase
			self._parseNode(node[0], net, net_i)
			#parse modifier
			self._parseNode(node[1], net, net_i)
		elif ntype == 'VP,V,NP':	#simple verb phrase
			#parse verb
			self._parseNode(node[0], net, net_i)
			#parse noun
			noun = net.add_node(KNode(''))
			net.nodes[net_i].links.append(KPort(noun))
			self._parseNode(node[1], net, noun)
		elif ntype == 'PP,P,NP':	#prepositional phrase
			#parse preposition
			prep = net.add_node(KNode(str(node[0][0])))
			net.nodes[prep].links.append(net_i)
			#parse noun phrase
			noun = net.add_node(KNode(''))
			net.nodes[prep].links.append(noun)
			self._parseNode(node[1], net, noun)
		elif ntype == 'NP,DT,N,PP':	#modified noun phrase
			net.nodes[net_i].name = str(node[0][0]) + ' ' + str(node[1][0])
			#parse modifier
			self._parseNode(node[2], net, net_i)
		elif ntype == 'NP,DT,N':	#noun with determinant
			net.nodes[net_i].name = str(node[0][0]) + ' ' + str(node[1][0])
		elif ntype == 'V':			#simple verb
			net.nodes[net_i].name = node[0]
		elif ntype == 'NP':			#simple noun
			net.nodes[net_i].name = node[0]
		else:
			print ntype
	#prints out the leaves of a node
	def print_tnode(self, node):
		if node == None:
			return ''
		if len(node) <= 1:
			return node[0]
		s = []
		for n in node:
			s.append(self.print_tnode(n))
		return ' '.join(s)
		#print len(node[0]), node[0][0]
	def __str__(self):
		s = '[\n  ' + '\n  '.join(['['+str(x)+'] '+str(self.nodes[x]) for x in xrange(0, len(self.nodes))]) + '\n]'
		return s

class KNode(object):
	"""Semantic node, holds relations to other nodes"""
	def __init__(self, name):
		self.name = name
		self.linked_to = []	#used if this node is linked to a linking node in a way
		self.links = []		#used if this nodes links other nodes together in a way
		self.cond = False	#for searching for a condition in many nodes
		self.ref = -1		#if node is referring to another node
	def __str__(self):
		s = 'Name: '+self.name
		if len(self.linked_to) > 0:
			s+= ' linked to: '+str(self.linked_to)
		if len(self.links) > 0:
			s+= ' links: [ '
			for l in self.links:
				s+= str(l) + ' '
			s+= ']'
		if self.ref > -1:
			s+= ' referring: '+str(self.ref)
		return s
	def __eq__(self, other):
		if self.name != other.name:
			return False
		if self.linked_to != other.linked_to:
			return False
		if not self.ref == other.ref:
			return False
		if len(self.links) != len(other.links):
			return False
		for i in xrange(0, len(self.links)):
			if not self.links[i] == other.links[i]:
				return False
		return True

class KPort(object):
	"""A sort of index describing what something links to"""
	def __init__(self, index, subs=[]):
		self.index = index
		self.subs = subs	#referring to a certain part(s) of this thing
		self.sel_sub = -1	#default to referring to the thing itself
	def set_sub(self, name):
		for i in xrange(0, len(self.subs)):
			if self.subs[i]['name'] == name:
				self.sel_sub = i
	def __str__(self):
		s = str(self.index)
		if self.sel_sub >= 0:
			s += '('+str(self.sel_sub)+')'
		return s
	def __eq__(self, other):
		if self.index != other.index:
			return False
		if self.subs != other.subs:
			return False
		if self.sel_sub != other.sel_sub:
			return False
		return True