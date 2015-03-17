#!/usr/bin/python
from knowledge_net import *

k = KNet()

#dogs are animals with fur
tmp = k.add_link([k.r('animal'), k.r('fur')], k.r('with'))
k.add_link([k.r('dog'), tmp], k.r('is'))

#animals are vertebrates
k.add_link([k.r('animal'), k.r('vertebrate')], k.r('is'))

#he likes the girl who wore the dress
tmp = k.add_link([k.r('girl'), k.r('dress')], k.r('wore'))
tmp.set_sub('girl')
k.add_link([k.r('he'), tmp], k.r('likes'))

print k
#are dogs vertebrates?
#print k.find_is(k.find('dog'), k.find('vertebrates'))