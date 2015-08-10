#!/usr/bin/python
from pprint import pprint
from collections import OrderedDict
import re

def parse_pages(txt):
	txt=txt[len("pages"):]
	dic=OrderedDict(i.split() for i in txt.strip().split('\n'))
	return dic

def parse_pageset(lines):
	results=[]
	for y in parse_pageset_yield(lines):
		results.append(OrderedDict(x.split(':') for x in y))
	return results

def parse_pageset_yield(lines):
	assert(lines[0]=="pagesets")
	lines=lines[1:]
	buf=[]
	for line in lines:
		if line.startswith("cpu:"):
			yield buf
			buf=[]
		buf.append(line)
	yield buf

def parse_zoneinfo(fname):
	nodes=[]
	p=re.compile("(?<=\S)+:?\s+")
	for node in parse_zoneinfo_node(fname):
		# print node
		# print "-------------------------"
		nodeinfo=parse_zoneinfo_yield(node)
		lines=[]
		nodedic=OrderedDict()
		for item in nodeinfo:
			# print item
			lines.append(item)
			if item[0].startswith("pages "):
				nodedic["pages"]=parse_pages("\n".join(item))
			elif item[0].startswith("pagesets"):
				nodedic["pagesets"]=parse_pageset(item)
			else:
				d=p.split("\n".join(item), 1)	
				nodedic[d[0]]=d[1]

		nodes.append(nodedic)
	return nodes

def parse_zoneinfo_yield(nodelines):
	# print nodelines
	pagestxt=[]
	for l in nodelines:
		line=l.strip()
		if line.startswith("pages "):
			pagestxt.append(line)
			continue
		
		elif line.startswith("pagesets"):
			yield pagestxt
			pagestxt=[]
			pagestxt.append(line)
			continue

		elif line.startswith("nr_"):
			yield pagestxt
			pagestxt=[]
			pagestxt.append(line)
			continue

		elif line.startswith("all_unreclaimable"):
			yield pagestxt
			pagestxt=[]
		
		if len(pagestxt) != 0:
			pagestxt.append(line)
			continue

		yield [line]


def parse_zoneinfo_node(fname):
  	with open(fname, 'r') as f:
  		buf=None
  	  	for line in f:
  			if line.startswith("Node"):
  				if buf is not None:
  					yield buf
 
				buf=[]
  			buf.append(line)
  		yield buf


if __name__ == '__main__':
	pprint(parse_zoneinfo("samples/zoneinfo.txt"))