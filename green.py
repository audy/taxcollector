#!/usr/bin/env python
# encoding: utf-8

import os
import sys
import string

# taxExemption - clades to exclude.
taxExemption = ['subspecies','subgenus','subfamily',
 'suborder','subclass','subphylum','superphylum','subkingdom','superspecies',
 'superfamily','superorder','superclass','superphylum',
 'no rank','tribe','authority','varietas','species group',
 'species subgroup','infaclass','original']
# concerned - clades to include in the final output (in order).
taxInclusion =  [ 'superkingdom','phylum','class','order','family','genus']
# Clade to stop at (seriously, you don't need mess with this.  Default = 1 for 'root')
stoplist = [1]

def main(argv):

  if len(argv)!= 6:
    print 'USAGE', argv[0], '<names.dmp> <nodes.dmp> <ProkMSA.txt> <greengenes.fas> <output.fas>'
    quit(2)

  hNames, hNodes, hProk, hDB, hOut = argv[1:]
  newID, namesList, = [], []
  rNames, Nodes, ProkIDs = {}, {}, {}
  Taxonomy = ''

  try:
    handle = open(hNames, 'r')
    print 'Opening', hNames
  except:
    print 'Error opening', hNames
    quit(2)
    
  for line in handle:
    line = line.split('\t|\t')
    taxid, name, type = line[0], line[1], line[3].replace('\t|\n','')
    taxid = int(taxid)
    if 'scientific name'==type:
      rNames[taxid] = name
      
  handle.close()
  
  try:
    handle = open(hNodes, 'r')
    print 'Opening', hNodes
  except:
    print 'Error opening', hNodes
    quit(2)
        
  for line in handle:
    taxID, parentid, type = line.split('\t|\t')[:3]
    taxID = int(taxID)
    parentid = int(parentid)
    Nodes[taxID] = [ parentid, type ]
    
  handle.close()
  
  try:
    handle = open(hProk, 'r')
    print 'Opening', hProk
  except:
    print 'Error opening', hProk
    quit(2)
    
  for line in handle:
    prokID, taxID = line.split('\t|\t')
    prokID, taxID = int(prokID), int(taxID)
    ProkIDs[prokID] = taxID
    
  handle.close()
  
  try:
    handle = open(hDB, 'r')
    output = open(hOut, 'w')
    print 'Opening', hDB, '&', hOut
  except:
    print 'Error opening', hDB, 'or', hOut
    quit(2)
    
  print 'Doing lots of stuff...'
      
  for line in handle:
    TaxList, idList, TaxDirt = [], [], {}
    Taxonomy = ''
    
    if line[:1]=='>':
      line = line.split(' ')
      ProkID, OriginalName = int(line[0][1:]), ' '.join(line[2:])
      
      if ProkID in ProkIDs:
        NewID = [ ProkIDs[ProkID], 'original' ]
      else:
        NewID = [ 1, 'no rank' ]
        
      idList.append(NewID)
      
      while 1:
        if NewID[0] in Nodes:
          NewID = [ Nodes[NewID[0]][0], Nodes[Nodes[NewID[0]][0]][1] ]
          if NewID[0] in stoplist:
            break
          else:
            idList.append( NewID )
        else:
          idList.append ( [1, ''] )
          break
        
      for i in range(len(idList)):
        TaxID, Clade = idList[i]
        if Clade == 'original':
          continue
        else:
          Name = rNames[TaxID]
        
        if Clade in taxInclusion:
          TaxDirt[Clade] = Name
          
      if 'genus' not in TaxDirt:
        TaxDirt['genus'] = OriginalName.strip()

      for i in range(len(taxInclusion)):
        Clade = taxInclusion[i]
        if Clade in TaxDirt:
          TaxList.append( [ i, TaxDirt[Clade] ] )     
        
      next = [0, '']
      hasfive = False
      
      for item in TaxList:
        if item[0] == 5:
          hasfive = True
        if item[0] == 6:
          duplicateme = item

      if hasfive is not True:
        TaxList.append([5, "\"" + duplicateme[1] + "\""])

      TaxList.sort()
      TaxList.reverse()     
            
      for item in TaxList:
        
        if next[0] - item[0] == 2:
          Taxonomy = '[' + str(next[0]-1) + ']\"' + next[1].strip("\"") + '\";' + Taxonomy
        next = item
        Taxonomy = '[' + str(item[0]) + ']' + item[1] + ';' + Taxonomy
          
      output.write('>' + Taxonomy.replace(' ','_') + '[6]' + OriginalName.replace(' ','_'))
      
    else:
      output.write(line)
    
    
  output.close()
  handle.close()
  
  print 'Lots of stuff done.'
      
  
if __name__=='__main__':
  main(sys.argv)
