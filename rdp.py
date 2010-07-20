#!/usr/bin/env python
# encoding: utf-8

''' RDP Taxonomy Collector (Elaborator)
	Austin Davis-Richardson, University of Florida, Dept. of Microbiology & Cell Science, Triplett Lab
	harekrishna@gmail.com

 	This script...
		... attempts to get return a full taxonomy from species names in the headers of the RDP database.
		... excludes levels of taxonomy in the list 'taxExemption' defined below.
		... only includes levels of taxonomy in the list 'taxInclusion' defined below.
		... Inserts numbers which represent the levels of taxonomy before their respecive names:
				0 = Superkingdom (Kingdom), ... 6 = Species
		... if a name cannot be found between TWO known names, this script will insert a "false" name which is the
			same as the name before it.
			i.e. [0]Bacteria;[1]Cyanobacteria;[2]"Cyanobacteria";[3]Oscillatoriales;[4]"Oscillatoriales";[5]Geitlerinema;[6]Geitlerinema sp. SP19606-11
'''

import os
import sys
import string

# Edit these as you wish. (case-sensitive!):
# taxExemption - levels of taxonomy to exclude.
taxExemption = ['subspecies','subgenus','subfamily','suborder','subclass','subphylum','subkingdom','superspecies','superfamily','superorder','superclass','superphylum','no rank','tribe','authority','varietas','species group','species subgroup','infaclass']
# concerned - levels of taxonomy to include in the final output (IN ORDER).
taxInclusion =  [ 'superkingdom','phylum','class','order','family','genus','species' ]


def main(argv):
	
	if not len(argv) == 5:
		print 'USAGE:', argv[0], '<names file> <nodes file> <RDP file> <output file>'
		quit(2)
	
	fnNames,fnNodes,fnRDP,fnOutput = argv[1:5]
	
	print 'Loading NCBI databases:', fnNames, fnNodes
	
	Names,rNames,Nodes = loadTax(fnNames, fnNodes)
	
	print 'Loading RDP database:', fnRDP
	#fastaDB = loadGreenGenes(fnRDP)
	fastaDB = loadRDP(fnRDP)
		
	print 'Searching...'
	
	for item in fastaDB:
		nom = item[0].replace(' ','')
		if nom in Names:
			item.append( getNames( getIDs(nom, Names, rNames, Nodes), rNames) )
		
	saveDB(fastaDB,fnOutput)
	

def saveDB(RDP,fnOutput):
	
	try: 
		output = open(fnOutput,'w')
	except: 
		print 'ERROR: unable to open file for output.'
		quit(2)
		
	print 'Saving:',fnOutput
	
	counter = 0
	
	for item in RDP:
		try: 
			output.write( '>' + item[2].replace(' ','_') + '\n' + item[1] )
			counter += 1
		except: pass
			
	print 'Saved', counter, 'records.'
		

def getNames(TaxIDs, rNames):
	
	taxdirt = {}
	taxlist = []
	taxonomy = ''
	
	for i in range(len(TaxIDs)):
		taxid, level = TaxIDs[i]
		name = rNames[taxid]
		
		if level not in taxExemption:
			if level in taxInclusion:
				taxdirt[level] =  name
				
	for i in range(len(taxInclusion)):
		level = taxInclusion[i]
		if level in taxdirt:
			taxlist.append( [ i,  taxdirt[level] ])
			
	next = [0, '']
	
	taxlist.reverse()
	
	for item in taxlist:
		if next[0] - item[0] == 2:
			taxonomy = '[' + str(next[0]-1) + ']\"' + next[1] + '\";'+ taxonomy
		next = item
		taxonomy = '[' + str(item[0]) + ']' + item[1] + ';' + taxonomy
				
	return taxonomy.strip(';')


def getIDs(name, Names, rNames, Nodes):
	
	idlist = []
	newid = []
	
#	for item in name:
#		if item in Names:
#			newid = [ Names[item], 'species' ] 
#			break
	
	if name in Names:
		newid = [ Names[name], 'species' ] 
	else:
		return 0
	
	idlist.append(newid)
	
	while not '1' == newid[0]:
		if newid[0] in Nodes:
			newid = Nodes[newid[0]]
			idlist.append([newid[0],Nodes[newid[0]][1]])
			
	return idlist

	
def loadGreenGenes(fnGG):
	
	try:
		GG = open(fnGG,'r')
	except:
		print 'ERROR: unable to open GreenGenes file for reading.'
		quit(2)
		
	Genes = []
	
	counter, sequence, header, Database = 0, '', '', []
	
	for line in GG:
		if line[:1] == '>':
			Genes.append([header, sequence])
			sequence, first, last = '','',''
			counter += 1
			try:
				header = line.split(' ')[2:]
			except: pass
		else:
			sequence += line
			
	print counter, 'GreenGenes records loaded from', fnGG
	return Genes
			

def loadRDP(fnRDP):
	
	try:
		fasta = open(fnRDP,'r')
	except:
		print 'ERROR: unable to open RDP file for reading.'
		quit(2)
		
	RDP = []
	
	counter, sequence, header, Database = 0, '', '', []
	
	for line in fasta:
		if line[:1] == '>':
			counter += 1
			RDP.append([header, sequence])
			sequence = ''
			header = line[line.find(' ')+1:line.find(';')].replace('(T)', '').strip()
		else:
			sequence += line
			
	fasta.close()
	
	print 'loaded', counter, 'RDP records.'
	return RDP
	

def loadTax(fnNames='names.dmp', fnNodes='nodes.dmp'):
	
	counter, rNames, Names, Nodes = 0, {}, {}, {}
	
	try:
		namesfile, nodesfile = open(fnNames, 'r'), open(fnNodes, 'r')
	except:
		print 'ERROR: unable to open Names and/or Nodes file for reading.'
		quit(2)
		
	for line in namesfile:
		line = line.split('\t|\t')
		taxid, name, nametype = line[0], line[1], line[3].replace('\t|\n', '')
		counter += 1
		if 'scientific name' == nametype:
			Names[name.replace(' ', '')] = taxid
			rNames[taxid] = name
			
	print 'loaded', counter, 'names from', fnNames
	
	counter = 0
	
	for line in nodesfile:
		counter += 1
		taxid, parentid, childtype = line.split('\t|\t')[:3]
		Nodes[taxid] = [parentid, childtype]
		
	print 'loaded', counter, 'nodes from', fnNodes
	
	nodesfile.close()
	namesfile.close()
	
	return Names, rNames, Nodes

	
if __name__ == '__main__':
	main(sys.argv)