#!/usr/bin/env python
# encoding: utf-8
"""
~~ fasta filter

    Filters Fasta Files based on an input word.

    i.e:

      > python filter.py input.fasta eukaryota

        filters out records with 'eukaryota' in the header.


~~ This script is case insensitive.


~~ By:
    Austin Davis-Richardson
      University of Florida
        Dept. of Microbiology & Cell Science
          The Laboratory of Eric W. Triplett
            Working under Adriana Giongo

"""

import sys
import os

class Fasta(object):
  """FASTA RECORD"""
  def __init__(self, header='', sequence=''):
    self.header = header
    self.sequence = sequence    


def main(argv):
  
  try:
    handle = open(argv[1],'r')
  except:
    print 'Hull Breach!', argv[1]
    
  Records, Counter = [], 1
    
  for line in handle:
    if '>' in line:
      record = Fasta()
      Records.append(record)
      record.header = line
      Counter += 1
    else:
      record.sequence += line[:-1]
      
  Records.append(record)
  
  handle.close()
  
  print 'Loaded', str(Counter), 'records.'
  Counter = 0
  
  try:
    handle = open(argv[2],'w')
  except:
    print 'Hull Breach!', argv[2]
    
  for record in Records:
    if argv[3].lower() in record.header.lower():
      Counter += 1
      continue
    else:
      handle.write(record.header)
      handle.write(record.sequence + '\n')

  handle.close()
  
  print 'Filtered', str(Counter), 'records.'

if __name__ == '__main__':
  main(sys.argv)

