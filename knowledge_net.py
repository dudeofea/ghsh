import copy

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
	def add_link(self, node_l, link_n):
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
	def __str__(self):
		s = '[\n  ' + '\n  '.join(['['+str(x)+'] '+str(self.nodes[x]) for x in xrange(0, len(self.nodes))]) + '\n]'
		return s

class KNode(object):
	"""Semantic node, holds relations to other nodes"""
	def __init__(self, name):
		self.name = name
		self.linked_to = []
		self.links = []
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
		if self.ref > -1:
			s+= '] referring: '+str(self.ref)
		return s

class KPort(object):
	"""A sort of index describing what something links to"""
	def __init__(self, index, subs):
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