import pickle

#get all combinations of tags
def combinate_tags(tags):
	if len(tags) > 1:
		for c in combinate_tags(tags[1:]):
			for t in tags[0][1:]:
				yield [(tags[0][0], t)] + c
	else:
		for t in tags[0][1:]:
			yield [(tags[0][0], t)]

class brute_tagger(object):
	def __init__(self, filename=None):
		self.tag_list = []
		if file != None:
			self.load_tags(filename)
	def tag(self, words):
		tags = []
		for i in xrange(0, len(words)):
			for t in self.tag_list:
				if words[i] == t[0]:
					tags.append(t)
					break
		for t in combinate_tags(tags):
			yield t
	def add_tag(self, word, tags):
		#see if it already exists
		index = -1
		for i in xrange(0,len(self.tag_list)):
			if word == self.tag_list[i][0]:
				index = i
				break
		if index < 0:	#new
			self.tag_list.append([word] + tags)
		else:			#old
			ext = list(set(tags) - set(self.tag_list[index][1:]))
			self.tag_list[index].extend(ext)
	def save_tags(self, filename):
		with open(filename, 'wb') as myfile:
			pickle.dump(self.tag_list, myfile, pickle.HIGHEST_PROTOCOL)
	def load_tags(self, filename):
		try:
			with open(filename, 'rb') as myfile:
				self.tag_list = pickle.load(myfile)
		except IOError as e:
			return