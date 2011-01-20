#!/usr/bin/env python

DESCRIPTION = """

    TaxCollector 2000
Austin G. Davis-Richardson
  harekrishna@gmail.com

"""

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
         
required = (1, 2, 3, 4, 5)

def main():
    """ For Glory! """
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
            record.header = phylogeny.replace(' ','_')
            p = True
            for r in required:
                if '[%s]' % r not in phylogeny:
                    skipped += 1
                    p = False
                    break
            if p:
                print record
                
    print >> sys.stderr, '%s names not found in NCBI database.' % skipped
                
def format_name(taxes):
    """ Formats Phylogeny """
    
    if 'genus' not in taxes:
        taxes['genus'] = '\"%s\"' % taxes['species']
    elif 'order' not in taxes:
        taxes['order'] = '\"%s\"' % taxes['genus']
    
    p, c = [], 1
        
    for i in phyla:
        try:
            n = '[%s]%s;' % (c, taxes[i])
            p.append(n)
        except KeyError:
            continue
        finally:
            c += 1
    return ''.join(p).rstrip(';')
    
def tax_collector(names, nodes):
    """ Returns a taxonomy given a name"""
    def collect_taxes(name):
        taxes = {}
        i = names.get_id(name)
        n = nodes.get_parent(i)
        taxes['species'] = ' '.join(name.split()[:2])
        taxes['_sbsp'] = name
    
        while i not in (None, 1):
            i = n['parent']
            n = nodes.get_parent(i) 
            t = n['childtype']
            name = names.get_name(i)
            taxes[t] = name

        return taxes
    return collect_taxes
    
class Names(object):
    """ Names Database """
    def __init__(self, handle):
        """ Load the Database """
        
        self.d, self.n = {}, {}
        
        for line in handle:
            line = line.split('\t|\t')
            taxid = int(line[0])
            name = line[1].replace(' ', '_')
            kind = line[3].replace('\t|\n', '')
            
            if 'scientific name' == kind:
                self.d[name] = taxid
                self.n[taxid] = name
                
    def get_name(self, q):
        """ Return a Name given an ID """
        try:
            return self.n[q]
        except KeyError:
            return None
        
    def get_id(self, name):
        """ Return an ID given a Name """
        try:
            return self.d[name.replace(' ', '_')]
        except KeyError:
            return None
    
class Nodes(object):
    """ Nodes Database """
    def __init__(self, handle):
        """ Load the Database"""
        self.n = {}
        for line in handle:
            taxid, parentid, childtype = line.split('\t|\t')[:3]
            taxid = int(taxid)
            parentid = int(parentid)
            self.n[taxid] = { 'parent': parentid, 'childtype': childtype }

    def get_parent(self, taxid):
        try:
            return self.n[taxid]
        except KeyError:
            return { 'parent': None, 'childtype': None }

class Fasta:
    """ Fasta Interpreter """
    def __init__(self, handle):
        self.handle = handle

    def __iter__(self):
        header = ''
        sequence = []
        for line in self.handle:
            if line[0] == '>':
                if sequence:
                    yield Dna(header, sequence)
                header, sequence = line[1:-1], []
            else:
                sequence.append(line.strip())
        yield Dna(header, sequence)

class Dna:
    ''' An object representing either a FASTA or FASTQ record '''
    def __init__(self, header, sequence, quality = False):
        self.header = header
        self.sequence = sequence
    def __str__(self):
        ''' returns a FASTA/Q formatted string '''
        return ('>%s\n%s') % (self.header, '\n'.join(self.sequence))

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print >> sys.stderr, "User Exited!"
        quit(-1)
