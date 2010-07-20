#!/usr/bin/env python
# encoding: utf-8

import os
import sys
import string

# taxExemption - clades to exclude.
taxExemption = ['subspecies','subgenus','subfamily',
 'suborder','subclass','subphylum','subkingdom','superspecies',
 'superfamily','superorder','superclass','superphylum',
 'no rank','tribe','authority','varietas','species group',
 'species subgroup','infaclass']
# concerned - clades to include in the final output (in order).
taxInclusion =  [ 'superkingdom','phylum','class','order','family','genus','species' ]


def main(argv):
	
	if not len(argv) == 6:
		print 'USAGE:',argv[0],'<names file> <nodes file> <ProkDB file> <RDP file> <output file>'
		quit(2)
	
	fnNames,fnNodes,fnProk,fnDB,fnOutput = argv[1:6]
	
	print 'Loading NCBI databases:',fnNames,fnNodes
	
	rNames,Nodes = loadTax(fnNames,fnNodes)
	
	print 'Loading GreenGenes database:',fnDB
	fastaDB = loadGreenGenes(fnDB)
	print 'Loading ProkMSA database:',fnProk
	ProkIDs = loadProkIds(fnProk)

	print 'Searching...'
		
	for item in fastaDB:
		prokID = item[0]
		if prokID in ProkIDs:
			item.append( getNames( getIDs(prokID,ProkIDs,Nodes),rNames) )
					
	saveDB(fastaDB,fnOutput)
	

def saveDB(RDP,fnOutput):
	
	try: 
		output = open(fnOutput,'w')
		handle = open('not found','w')
	except: 
		print 'ERROR: unable to open file for output.'
		quit(2)
		
	print 'Saving:',fnOutput
	
	counter = 0
	
	for item in RDP:
		try: 
			output.write( '>' + item[2].replace(' ','_') + '\n' + item[1] )
			counter += 1
		except:
			handle.write( '>' + item[0] + '\n' )
			
	print 'Saved',counter,'records.'
		
	handle.close()
	output.close()

def getNames(TaxIDs,rNames):
	
	taxdirt = {}
	taxlist = []
	taxonomy = ''
	lastname = ''	
	
	for i in range(len(TaxIDs)):
		taxid,level = TaxIDs[i]
		if taxid in rNames:
			name = rNames[taxid]
		else:
			name = ''
		
		if level not in taxExemption:
			if level in taxInclusion:
				taxdirt[level] = name
				
	for i in range(len(taxInclusion)):
		level = taxInclusion[i]
		if level in taxdirt:
			taxlist.append( [ i, taxdirt[level] ])
			
	last = [0,'']
	
	for item in taxlist:
		if item[0] - last[0] == 2:
			taxonomy += '[' + str(last[0]+1) + ']\"' + last[1] + '\";'
		last = item
		taxonomy += '[' + str(item[0]) + ']' + item[1] + ';'
				
	return taxonomy.strip(';')


def getIDs(prok,ProkIDs,Nodes):
	
	idlist = []
	newid = []
	stoplist = ['1']
		
	if prok in ProkIDs:
		newid = [ ProkIDs[prok],'species' ]
		
	else:
		return 0
	
	idlist.append(newid)
	
	while not newid[0] in stoplist:
		if newid[0] in Nodes:
			newid = Nodes[newid[0]]
			idlist.append([newid[0],Nodes[newid[0]][1]])
		else:
			idlist.append( [1,''] )
			return idlist
			break
			
	return idlist


def loadProkIds(fnProk):
	
	try:
		handle = open(fnProk,'r')
	except:
		print 'Error: unable to open ProkIDs file for reading.'
		quit(2)
		
	ProkIDs = {}
	prokID,taxID = '',''
	counter = 0 
	
	for line in handle:
		prokID,taxID = line.split('\t|\t')
		taxID = taxID.strip('\n')
		ProkIDs[prokID] = taxID
		counter +=1
	
	print 'Loaded',counter,'ProkMSA > Tax IDs'
	return ProkIDs
	
	
	
def loadGreenGenes(fnGG):
	
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
			
	print counter,'GreenGenes records loaded from',fnGG
	
	return Genes
			

def loadRDP(fnRDP):
	
	try:
		fasta = open(fnRDP,'r')
	except:
		print 'ERROR: unable to open RDP file for reading.'
		quit(2)
		
	RDP = []
	
	counter,sequence,header,Database = 0,'','',[]
	
	for line in fasta:
		if line[:1] == '>':
			counter += 1
			RDP.append([header,sequence])
			sequence = ''
			header = line[line.find(' ')+1:line.find(';')].replace('(T)','').strip()
		else:
			sequence += line
			
	fasta.close()
	
	print 'loaded',counter,'RDP records.'
	return RDP
	

def loadTax(fnNames='names.dmp',fnNodes='nodes.dmp'):
	
	counter,rNames,Names,Nodes = 0,{},{},{}
	
	try:
		namesfile,nodesfile = open(fnNames,'r'),open(fnNodes,'r')
	except:
		print 'ERROR: unable to open Names and/or Nodes file for reading.'
		quit(2)
		
	for line in namesfile:
		line = line.split('\t|\t')
		taxid,name,nametype = line[0],line[1],line[3].replace('\t|\n','')
		counter += 1
		if 'scientific name' == nametype:
		#	Names[name.replace(' ','')] = taxid
			rNames[taxid] = name
			
	print 'loaded',counter,'names from',fnNames
	
	counter = 0
	
	for line in nodesfile:
		counter += 1
		taxid,parentid,childtype = line.split('\t|\t')[:3]
		Nodes[taxid] = [parentid,childtype]
		
	print 'loaded',counter,'nodes from',fnNodes
	
	nodesfile.close()
	namesfile.close()
	
	return rNames,Nodes

	
if __name__ == '__main__':
	main(sys.argv)