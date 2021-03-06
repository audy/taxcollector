# how we want our taxonomy to look
phyla = [ 'superkingdom',
          'phylum',
          'class',
          'order',
          'family',
          'genus',
          'species',
          '_sbsp'
         ]

# levels to create psuedonymns for (currently not enabled)
recycled_names = [
    'superkingdom',
    'class',
    'order',
    'family',
    'genus',
    'species'
    ]

def format_name(taxes):
    """ Formats Phylogeny """

    for level in reversed(recycled_names):
        if level not in taxes:
            # TODO make this an option:
            #new_name = taxes[recycled_names[recycled_names.index(level)+1]]
            #taxes[level] = '\"%s\"' % new_name.strip('\"')
            taxes[level] = 'null'

    p, c = [], 0

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

    def __iter__(self):
        for k in self.n:
            yield (k, self.n[k])

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
        self.accession = header.split(';')[-1].strip()
        self.orig_name = ' '.join(header.split(';')[0].split()[1:])
        self.sequence = sequence
    def __str__(self):
        ''' returns a FASTA/Q formatted string '''
        return ('>%s\n%s') % (self.header, '\n'.join(self.sequence))
