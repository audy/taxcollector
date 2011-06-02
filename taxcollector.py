#!/usr/bin/env python
from taxcollector import *
import sys

phyla = [ 'superkingdom',
          'phylum',
          'class',
          'order',
          'family',
          'genus',
          'species',
          '_sbsp'
         ]

recycled_names = [ # In Order!
    'superkingdom',
    'class',
    'order',
    'family',
    'genus',
    'species'
    ]
         
required = (1, 2, 3, 4, 5)

def main():

    try:
        names = sys.argv[1] 
        nodes = sys.argv[2]
        fasta = sys.argv[3]
    except IndexError:
        print >> sys.stderr, 'USAGE: %s names nodes fasta out' % sys.argv[0]
        quit(-1)
            
    with open(names) as handle:
        names = Names(handle)
            
    with open(nodes) as handle:
        nodes = Nodes(handle)

    collect_taxes = tax_collector(names, nodes)

    with open(fasta) as handle:
        skipped = 0
        records = Fasta(handle)
        for record in records:
            h = record.header
            name = h[h.find(' ')+1:h.find(';')].replace('(T)', '').strip()
            taxes = collect_taxes(name)
            phylogeny = format_name(taxes)
            record.header = "%s[8]%s|%s" % (phylogeny.replace(' ', '_'),
                                    record.orig_name.replace(' ', '_'),
                                    record.accession)
            p = True
            for r in required:
                if '[%s]' % r not in phylogeny:
                    skipped += 1
                    p = False
                    break
            if p:
                print record
                
    print >> sys.stderr, '%s names not found in NCBI database.' % skipped
    
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print >> sys.stderr, "User Exited!"
        quit(-1)