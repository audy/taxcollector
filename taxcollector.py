#!/usr/bin/env python
from taxcollector import *
import sys
    
skip_if = [
    'eukaryota',
    'eukarya',
    'clone',
    'plasmid',
    'vector',
    'uncultured'
]
         
required = (1, 2, 3, 4, 5)

def main():

    # parse arguments
    try:
        names = sys.argv[1] 
        nodes = sys.argv[2]
        blast = sys.argv[3]
        gi_to_taxid = sys.argv[4]
    except IndexError:
        print >> sys.stderr, 'USAGE: %s names nodes fasta out' % sys.argv[0]
        quit(-1)

    # load gi_to_taxid database
    with open(gi_to_taxid) as handle:
        gi_to_taxid = load_ncbi_taxdump(handle)

    # load names database.
    with open(names) as handle:
        names = Names(handle)
    
    # load nodes database
    with open(nodes) as handle:
        nodes = Nodes(handle)
    
    # create a function to collect taxonomic description given
    # names and nodes databases from NCBI
    collect_taxes = tax_collector(
                            names=names,
                            nodes=nodes,
                            gi_to_taxid=gi_to_taxid)

    # collect RDP database
    with open(blast) as handle:
        skipped = 0
        records = Fasta(handle)
        for line in handle:
            line = line.strip().split("\t")
            gid = int(line[1].split('|')[1])
            
            taxes = collect_taxes(gi = gid)
            phylogeny = format_name(taxes)
            taxonomy = "%s" % phylogeny.replace(' ', '_')
            line[1] = "%s\t%s" % (line[1], taxonomy)
            print "\t".join(line)
                        
    # tell the user how bad we did            
    print >> sys.stderr, '%s names not found in NCBI database.' % skipped
    
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print >> sys.stderr, "User Exited!"
        quit(-1)