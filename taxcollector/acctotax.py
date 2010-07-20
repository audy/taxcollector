#!/usr/bin/env python
# encoding: utf-8
"""
Acc to Tax:

Generates a flat-file database for use in green.py

Database contains ProkMSA IDs from the GreenGenes Database & their corresponding NCBI taxids.
"""

import sys
import os
import string


def main(argv):

	taxi, prokMSA = '', ''

	try:
		handle = open(argv[1],'r')
		outtie = open(argv[1] + 'out','w')
	except:
		print 'USAGE:', argv[0], 'inputfile'
		
	print 'Generating proktable from', argv[1]
		
	for line in handle:
		if line[:12] == 'ncbi_tax_id=':
			taxi = line[12:]
		if line[:11] == 'prokMSA_id=':
			prokMSA = line[11:].strip()
			outtie.write(prokMSA + '\t|\t' + taxi)

		
	print 'Done generating.'
	print 'Proktable saved as:', argv[1] + 'out'		
	
	handle.close()
	outtie.close()
		
		
		


if __name__ == '__main__':
	main(sys.argv)

