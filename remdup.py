#!/usr/bin/env python

# remdup.py
# Austin Davis-Richardson
# adavisr@ufl.edu

# This here script combines two fasta files, making sure that there are no duplicate (headers)
# If there are, then the record with the larger sequence is kept in the out-put file
# USAGE: python remdup.py <fasta file 1> <fasta file 2> <output file>
# Should work on any two fasta files with similar header formats.

import sys

def main(argv):
	try:
		first = open(argv[1],'r')
		second = open(argv[2],'r')
		outfile = open(argv[3],'w')
	except:
		print 'USAGE: python', argv[0], '<fasta file 1> <fasta file 2> <output file>'
		quit(2)
		
	print 'Trabajando...',
		
	rdpList = readFasta(first)
	genesList = readFasta(second)
	bothLists = {}
	counter = 0
	
	for record in rdpList:
		bothLists[record.name] = [ record.sequence ]
		
	for record in genesList:
		if record.name in bothLists:
			bothLists[record.name].append( record.sequence )
		else:
			bothLists[record.name] = [ record.sequence ]
	
	for key in bothLists:
		outfile.write( key + '\n' )
		if len(bothLists[key]) > 1:
			counter  +=1
		outfile.write( max(bothLists[key]) + '\n' )
		
	print 'Found', counter, 'duplicates.'
	print 'Saved as', argv[3]
	
class Fasta:
	def __init__(self, name, sequence):
		self.name = name
		self.sequence = sequence
	
def readFasta(file):
    items = []
    index = 0
    for line in file:
        if line.startswith(">"):
           if index >= 1:
               items.append(aninstance)
           index+=1
           name = line.strip()
           seq = ''
           aninstance = Fasta(name, seq)
        else:
           seq += line.strip()
           aninstance = Fasta(name, seq)

    items.append(aninstance)
    return items


if __name__ == '__main__':
	main(sys.argv)
