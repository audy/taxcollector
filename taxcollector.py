#!/usr/bin/env python3
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
        fasta = sys.argv[3]
    except IndexError:
        print(f'USAGE: {sys.argv[0]} names nodes fasta out', file=sys.stderr)
        quit(-1)

    # load names database.
    with open(names) as handle:
        names = Names(handle)

    # load nodes database
    with open(nodes) as handle:
        nodes = Nodes(handle)

    # create a function to collect taxonomic description given
    # names and nodes databases from NCBI
    collect_taxes = tax_collector(names, nodes)

    # collect RDP database
    with open(fasta) as handle:
        skipped = 0
        records = Fasta(handle)
        for i, record in enumerate(records):
            h = record.header
            name = h[h.find(' ')+1:h.find(';')].replace('(T)', '').strip()
            taxes = collect_taxes(name)
            phylogeny = format_name(taxes)
            record.header = "%s;[8]%s|%s|%s" % (phylogeny.replace(' ', '_'),
                                    record.orig_name.replace(' ', '_'),
                                    record.accession, i)
            # p = print?
            p = True
            # make sure taxonomic description is complete enough
            for r in required:
                if '[%s]' % r not in phylogeny:
                    skipped += 1
                    p = False
                    break
            if p:
                # don't print record if certain words are in name
                # these records are in skip_if
                for word in skip_if:
                    if word.upper() in record.header.upper():
                        p = False
                        break
            # yay our record is good, print it!
            if p:
                print(record)

    # tell the user how bad we did
    print(f"{skipped} names not found in NCBI database", file=sys.stderr)

if __name__ == '__main__':
    main()
