import copy

class KNet(object):
	"""Net of knowledge composed of nodes linked to each other"""
	def __init__(self):
		self.nodes = []
	def add_node(self, node):
		self.nodes.append(node)
		return len(self.nodes)-1
	def get(self, index):
		return self.nodes[index]
	def add_link(self, node1_i, node2_i, link):
		link.node2 = node2_i
		self.nodes[node1_i].links.append(link)
		link_c = copy.deepcopy(link)
		link_c.node2 = -1
		link_c.node1 = node1_i
		self.nodes[node2_i].links.append(link_c)
	#find node index by name
	def find(self, name):
		for x in xrange(0, len(self.nodes)):
			if self.nodes[x].name == name:
				return x
		return -1
	#find if node1 is node2
	def find_is(self, n1, n2):
		if n1 < 0 or n2 < 0:
			return False
		#blank conditions first
		for n in self.nodes:
			n.cond = False
		#we is us
		us = self.nodes[n2]
		us.cond = True
		return self._find_is(us, n1)
	#recursive function to find is
	def _find_is(self, us, n2):
		#look for all subset type links
		for l in us.links:
			if l.node2 == n2:
				return True		#done
			if l.node2 >= 0 and issubclass(type(l), AreKLink):
				#further links
				return self._find_is(self.nodes[l.node2], n2)
		#nothing :(
		return False	#done for this level
	def __str__(self):
		s = '[\n  ' + '\n  '.join(['['+str(x)+'] '+str(self.nodes[x]) for x in xrange(0, len(self.nodes))]) + '\n]'
		return s

class KNode(object):
	"""Semantic node, holds relations to other nodes"""
	def __init__(self, name):
		self.name = name
		self.links = []
		self.cond = False	#for searching for a condition in many nodes
	def __str__(self):
		s = 'Name: '+self.name
		s+= '   Links: '+', '.join([str(x) for x in self.links])
		return s

class KLink(object):
	"""A link from one KNode to another"""
	def __init__(self):
		self.node1 = -1		#main node
		self.node2 = -1		#referring node

#something IS something else, somethings can be many other things
#this is similar to WithKLink minus the 'with'. pure subset
class AreKLink(KLink):
	#node1 <-is- node2
	def __str__(self):
		s = ''
		if self.node1 < 0:
			s += 'me'
		else:
			s += 'node '+str(self.node1)
		s += ' <-is- '
		if self.node2 < 0:
			s += 'me'
		else:
			s += 'node '+str(self.node2)
		return s

#the link explaining the direct combination
#of 2 things making another thing. conditional subset
class WithKLink(AreKLink):
	#node1 + node_c -> node2
	def __init__(self, node_c):
		super(WithKLink, self).__init__()
		self.node_c = node_c
	def __str__(self):
		s = ''
		if self.node1 < 0:
			s += 'me'
		else:
			s += 'node '+str(self.node1)
		s += ' w/ node '+str(self.node_c)+' -> '
		if self.node2 < 0:
			s += 'me'
		else:
			s += 'node '+str(self.node2)
		return s