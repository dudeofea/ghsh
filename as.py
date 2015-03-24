#!/usr/bin/python
from knowledge_net import *

k = KNet()

#dogs are animals with fur
tmp = k.add_link([k.r('with'), k.r('animal'), k.r('fur')])
k.add_link([k.r('is'), k.r('dog'), tmp])

#animals are vertebrates
k.add_link([k.r('is'), k.r('animal'), k.r('vertebrate')])

#he likes the girl who wore the dress
tmp = k.add_link([k.r('wore'), k.r('girl'), k.r('dress')])
tmp.set_sub('girl')
k.add_link([k.r('likes'), k.r('he'), tmp])

print k
#are dogs vertebrates?
#print k.find_is(k.find('dog'), k.find('vertebrates'))