import sys
from taxcollector import Dna, Fasta

# Remove duplicates, and simultaneously
# filter out reads with the following in the headers:

# Invoke like this:

# Case insensitive
filtered_words = set(('eukarya', 'clone', 'plasmid', 'cloning_vector', 'chloroplast'))

try:
    filename = sys.argv[1]
except IndexError:
    print >> sys.stderr, "usage: %s input.fasta > output.fasta" % sys.argv[0]

print >> sys.stderr, "removing words: (%s), and duplciates from %s" % \
    (' '.join(filtered_words), filename)

sequences = set()
c, t = 0, 0
with open(sys.argv[1]) as handle:
    for record in Fasta(handle):
        if ''.join(record.sequence) not in sequences:
            for word in filtered_words:
                if word in record.header.lower():
                    c += 1
                    continue
            sequences.add(''.join(record.sequence))
            t += 1
            print record
        else:
            c += 1
            
print >> sys.stderr, "filtered %s out of %s records" % (c, t)