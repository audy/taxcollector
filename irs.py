#!/usr/bin/env python

DESCRIPTION = """

    TaxCollector 2000
Austin G. Davis-Richardson
  harekrishna@gmail.com

"""

import sys

def main():
    """ """
    names = 'names.dmp'
    nodes = 'nodes.dmp'
    
    print 'loading %s' % names
    with open(names) as handle:
        names = Names(handle)
        
    print names.get_name(100)
        
    print 'loading %s' % nodes
    with open(nodes) as handle:
        nodes = Nodes(handle)
        
    print nodes
    
    # Should we only load Names we care about?
    # Maybe we should just index our names and nodes files.
    
class Names(object):
    """ Names Database """
    def __init__(self, handle):
        """ Load the Database """
        
        self.d, self.n = {}, {}
        
        for line in handle:
            line = line.split('\t|\t')
            taxid = int(line[0])
            name = line[1].replace(' ', '')
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
            return self.d[name]
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
            self.n[taxid] = { 'parent': parentid, 'type': childtype }
    def get_parent(self, taxid):
        try:
            return self.n[taxid]
        except KeyError:
            return None


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print >> sys.stderr, "User Exited!"
        quit(-1)