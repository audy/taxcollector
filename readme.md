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

This software is distributed under the [GNU GPL 2.0 software license](http://www.gnu.org/licenses/gpl.html).

Please Cite: Giongo A., Davis-Richardson A.G., Crabb D.B., Triplett E.W.
TaxCollector: Modifying Current 16S rRNA Databases for the Rapid Classification
at Six Taxonomic Levels. *Diversity*. __2010__; 2(7):1015-1025.
