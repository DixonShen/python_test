#coding=utf-8
__author__ = 'DixonShen'

import codecs

l1 = [1,2,3,4,5,6,7,8]
l2 = [1,3,5,7]
l3 = [ x for x in l1 if x not in l2]
print l3
