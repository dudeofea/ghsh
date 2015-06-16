import pickle, nltk

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
	def __init__(self, filename=None, train=False):
		self.tag_list = ([], [])
		if filename != None:
			self.load_tags(filename)
		self.train = train
	def tag(self, words):
		tags = []
		for i in xrange(0, len(words)):
			try:
				j = self.tag_list[0].index(words[i])
			except ValueError:
				j = -1
			if j >= 0:
				tags.append([words[i]]+self.tag_list[1][j])
			elif self.train:
				print "added new word:", words[i]
				tag = [nltk.pos_tag([words[i]])[0][1]]
				self.add_tag(words[i], tag)
				tags.append([words[i]] + tag)
			else:
				tags.append([words[i]])
		for t in combinate_tags(tags):
			yield t
	def add_tag(self, word, tags):
		#see if it already exists
		try:
			index = self.tag_list[0].index(word)
		except ValueError:
			index = -1
		if index < 0:	#new
			self.tag_list[0].append(word)
			self.tag_list[1].append(tags)
		else:			#old
			ext = list(set(tags) - set(self.tag_list[1][index][1:]))
			self.tag_list[1][index].extend(ext)
	def save_tags(self, filename):
		with open(filename, 'wb') as myfile:
			pickle.dump(self.tag_list, myfile, pickle.HIGHEST_PROTOCOL)
	def load_tags(self, filename):
		try:
			with open(filename, 'rb') as myfile:
				self.tag_list = pickle.load(myfile)
		except IOError as e:
			return