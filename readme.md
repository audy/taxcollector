# TaxCollector

[Austin G. Davis-Richardson](mailto:harekrishna@gmail.com)

---

For the original TaxCollector ([publication](http://www.mdpi.com/1424-2818/2/7/1015/)), please
check out the ["publication" branch](http://github.com/audy/taxcollector/tree/publication).

## About

TaxCollector is a tool for modifying the Ribosomal Database Project (RDP) 16S
rRNA database. The RDP database is a fasta file with 16S rRNA sequences. The
headers are terribly non-descriptive. Using the NCBI names and nodes databases,
this script can create detailed taxonomic descriptions.

For example, this script takes the default RDP header:

    >S001018666 uncultured Acidobacteria bacterium; 2YMLF03; EF630306

And converts it to this:

    >[0]Bacteria;[1]Acidobacteria;[2]Holophagae;[3]Holophagales;[4]Holophagaceae;[5]Geothrix;[6]Geothrix_fermentans;[7]Geothrix_fermentans[8]Geothrix_fermentans_(T)|U41563

Notice that the Genus is in "quotes." This means that there was no entry for
Genus in the NCBI names and nodes databases. In this case, TaxCollector will
make one up, recycling the previous name. This only happens for Genus and
Order.

This can be useful for some people. For others, not.

By default, TaxCollector filters out entries with the following in their
taxonomy:

    'eukaryota'
    'eukarya'
    'clone'
    'plasmid'
    'vector'
    'uncultured'

If you don't want this, change it in the taxcollector.py file

## Invocation

### Requirements

- Python 3.7

### For the lazy:

Type `make`.

This will download necessary databases and compile you a taxcollector.fa file

### Otherwise

invoke _comme ca_

    python taxcollector.py names.dmp nodes.dmp input.fasta > output.fasta

You can get names.dmp and nodes.dmp from [NCBI's FTP site](ftp://ftp.ncbi.nih.gov/taxdump.tar.gz).

My favorite way to do this is by typing

    curl ftp://ftp.ncbi.nih.gov/pub/taxonomy/taxdump.tar.gz | gunzip | tar -xvf names.dmp nodes.dmp

The FASTA file must come from RDP (http://rdp.cme.msu.edu).

# License

The MIT License (MIT)
Copyright (c) 2010-2018 Giongo A., Davis-Richardson A.G., Crabb D.B., Triplett E.W.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

Please Cite: Giongo A., Davis-Richardson A.G., Crabb D.B., Triplett E.W.
TaxCollector: Modifying Current 16S rRNA Databases for the Rapid Classification
at Six Taxonomic Levels. *Diversity*. __2010__; 2(7):1015-1025.
