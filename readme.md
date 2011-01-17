# TaxCollector 2000

Austin G. Davis-Richardson  
[harekrishna@gmail.com](mailto:harekrishna@gmail.com)

---

## Invocation

Make it work _comme ca_

	python taxcollector.py names.dmp nodes.dmp input.fasta > output.fasta
	
You can get names.dmp and nodes.dmp from NCBI's FTP site [ftp://ftp.ncbi.nih.gov/taxdump.tar.gz).

The FASTA file must come from RDP [http://rdp.cme.msu.edu]. For GreenGenes,
get [version 1.0.0](https://github.com/audy/taxcollector/tree/1.0.0).

### For the lazy

I've provided a super-convenient Rakefile for building the RDP database.

In the taxcollector directory, simply type:

rake bacteria/archaea/both to download all required databases (if needed), and create the corresponding TaxCollector database.

(This requires that you have [Rake](http://rubyforge.org/projects/rake/) installed. Provided with Mac OSX and most UNIXy systems)