#!/usr/bin/env python
# encoding: utf-8
"""
Austin Davis-Richardson
adavisr@ufl.edu

Removes cloned or unculted rRNA sequences from a greengenes file.

usage: python cloneremover.py <input file> <output file>

"""

import sys
import os
import string

def main(argv):

	fasta = []
	
	try:
		handle = open(argv[1],'r')
		outfile = open(argv[2],'w')
	except:
		print 'USAGE:', argv[0], '<input file> <output file>'
		
	print 'Loading and removing clones from fasta file'
	
	for line in handle:
		if line[:1] == '>':
			header = line
		else:
			sequence = line
			fasta.append( { 'header': header, 'sequence': sequence } )
	
	counter = 0
	
	for item in fasta:
		if 'clone' in item['header']:
			counter += 1
			continue
		else:
			outfile.write( item['header'] + item['sequence'] )
		
	handle.close()
	outfile.close()
			
	print 'removed', counter, 'records from fasta database and saved as', argv[2]

if __name__ == '__main__':
	main(sys.argv)

