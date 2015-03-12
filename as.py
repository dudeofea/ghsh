#!/usr/bin/python
from knowledge_net import *

k = KNet()
k.add_node(KNode('animal'))
k.add_node(KNode('dog'))
k.add_node(KNode('fur'))
k.add_node(KNode('vertebrates'))
#dogs are animals with fur
k.add_link(0, 1, WithKLink(2))

#animals are vertebrates
k.add_link(3, 0, AreKLink())

#print k
#are dogs vertebrates?
print k.find_is(k.find('dog'), k.find('vertebrates'))