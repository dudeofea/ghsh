#!/usr/bin/python
class Thing:
	def __init__(self, name):
		self.name = name
	def __str__(self):
		return self.name

class Knowledge:
	k = []
	def add_thing(self, t):
		self.k.append(t)
	def print_things(self):
		for a in self.k:
			print a
	def interact(self):
		print "hi, what do you want?"
		q = raw_input()
		q = q.split(' ') #get array of words
		if q[0] == 'get':
			#get a number of something
			if q[1] == 'all':
				#get all of something
				
			else:
				print "I don't know how to get",q[1],"of something"
		else:
			print "I don't know what",q[0],"is."

k = Knowledge()
k.add_thing(Thing("horse"))
k.add_thing(Thing("cow"))
k.add_thing(Thing("chicken"))
k.print_things()
k.interact()