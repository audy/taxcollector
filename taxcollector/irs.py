#!/usr/bin/env python

class Options:
    ''' cant use options parsing library because usage needs to be the same
as it was described in the paper. '''
    def __init__(self):
        import sys
        assert len(sys.argv) == 5
        self.names, self.nodes, self.infile, self.outfile = sys.argv[1:]

def main():
    pass

if __name__ == '__main__':
    main()