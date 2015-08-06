#!/usr/bin/python

import sys
from collections import defaultdict
from pprint import pprint
from HTMLParser import HTMLParser

class MyParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.stack=[]
		self.depth=0
		self.content=[]

	def handle_starttag(self, tag, attrs):
		# print "start", (tag, attrs)
		self.stack.append([tag, None])

	def handle_data(self, data):
		# print "data %r" % data
		top=self.stack[-1]
		top[1]=data

		
	def handle_endtag(self, tag):
		# print self.stack
		top=self.stack.pop()

		if len(self.stack)>0:
			parent=self.stack[-1]

			if parent[1] == None:
				parent[1] = {}

			if tag in parent[1]:
				old=parent[1][tag]
				parent[1][tag]=[]
				parent[1][tag].append(old)
				parent[1][tag].append(top[1])
			else:
				parent[1][tag]=top[1]

		# pprint(self.stack)
		pprint(top)

if __name__ == '__main__':
	raw_txt=sys.stdin.read()
	raw_txt=raw_txt.replace('\n','').replace('\t','').replace(' ','')
	mp=MyParser()
	mp.feed(raw_txt)
	mp.close()

	pprint(mp.stack)