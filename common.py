#!/usr/bin/env python
# encoding: utf-8

# Austin G. Davis-Richardson
# harekrishna@gmail.com
# Triplett Lab
# University of Florida
# Gainesville, FL

import sys

# Edit these as you wish. (case-sensitive!):
# taxExemption - levels of taxonomy to exclude.
taxExemption = ['subspecies','subgenus','subfamily','suborder','subclass',
'subphylum','subkingdom','superspecies','superfamily','superorder',
'superclass','superphylum','no rank','tribe','authority','varietas',
'species group','species subgroup','infaclass']

# concerned - levels of taxonomy to include in the final output (IN ORDER).
taxInclusion =  [ 'superkingdom','phylum','class',
'order','family','genus','species' ]

def main_rdp(argv):
	''' main() for RDP '''
	if not len(argv) == 5:
		print 'USAGE:', argv[0], '<names file> <nodes file> <RDP file> <output file>'
		quit(2)
	fnNames, fnNodes, fnRDP, fnOutput = argv[1:5]
	
	print 'Loading NCBI Names: %s & Nodes: %s' % (fnNames, fnNodes)
	Names, rNames, Nodes = loadTax(fnNames, fnNodes)
	
	print 'Loading RDP database: %s' % fnRDP
	fastaDB = loadRDP(fnRDP)
		
	print 'Searching...'
	for item in fastaDB:
		nom = item[0].replace(' ','')
		if nom in Names:
			item.append( getNames( getIDs(nom, Names, rNames, Nodes), rNames) )
	
	print 'Saving...'
	saveDB(fastaDB,fnOutput)
	

def main_gg(argv):
    ''' main() for GreenGenes '''
	if not len(argv) == 6:
		print 'USAGE:',argv[0],'<names file> <nodes file> <ProkDB file> <RDP file> <output file>'
		quit(2)

	fnNames, fnNodes, fnProk, fnDB, fnOutput = argv[1:6]

	print 'Loading NCBI Names: %s & Nodes: %s' % (fnNames, fnNodes)
	rNames, Nodes = loadTax(fnNames,fnNodes)

	print 'Loading GreenGenes database: %s' % fnDB
	fastaDB = loadGreenGenes(fnDB)
	
	print 'Loading ProkMSA database: %s', % fnProk
	ProkIDs = loadProkIds(fnProk)

	print 'Searching...'
	for item in fastaDB:
		prokID = item[0]
		if prokID in ProkIDs:
			item.append( getNames( getIDs(prokID,ProkIDs,Nodes),rNames) )

	saveDB(fastaDB,fnOutput)


def saveDB(RDP, fnOutput):
	''' Saves TaxCollected Database'''
	try: 
		output = open(fnOutput,'w')
	except: 
		print 'ERROR: unable to open file for output.'
		quit(2)
	print 'Saving: %s' % fnOutput
	counter = 0
	for item in RDP:
		try: 
			output.write( '>' + item[2].replace(' ','_') + '\n' + item[1] )
			counter += 1
		except: pass
	print 'Saved %s records.' % counter
		

def getNames(TaxIDs, rNames):
	''' gets Names from a list of TaxIDs '''
	taxdirt, taxlist, taxonomy = {}, [], ''
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
	''' Gets IDs given a name '''
	idlist, newid = [], []
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
    ''' loads GreenGenes database. '''
	try:
		GG = open(fnGG,'r')
	except:
		print 'ERROR: unable to open GreenGenes file for reading.'
		quit(2)

	Genes = []
	counter,sequence,prokid,Database = 0,'','',[]
	for line in GG:
		if line[:1] == '>':
			Genes.append([prokid,sequence])
			sequence,first,last = '','',''
			counter += 1
			try:
				prokid = line.split(' ')[0][1:]
			except: pass
		else:
			sequence += line
	print ' %s GreenGenes records loaded from %s' %  (counter, fnGG)

	return Genes


def loadRDP(fnRDP):
	''' loads RDP database. '''
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
	print 'loaded %s RDP records.' % counter
	return RDP
	

def loadTax(fnNames='names.dmp', fnNodes='nodes.dmp'):
	'''  loads Taxonomy Databases '''
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
	print 'loaded %s names from %s' % (counter, fnNames)
	
	counter = 0
	for line in nodesfile:
		counter += 1
		taxid, parentid, childtype = line.split('\t|\t')[:3]
		Nodes[taxid] = [parentid, childtype]
	print 'loaded %s nodes from %s' %  (counter, fnNodes)
	nodesfile.close()
	namesfile.close()
	
	return Names, rNames, Nodes