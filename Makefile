taxcollector.fa: rdp.fa names.dmp nodes.dmp
	python taxcollector.py names.dmp nodes.dmp rdp.fa > taxcollector.fa

rdp.fa:
	curl http://rdp.cme.msu.edu/download/release10_30_unaligned.fa.gz | gunzip > rdp.fa

%.dmp:
	curl ftp://ftp.ncbi.nih.gov/pub/taxonomy/taxdump.tar.gz | gunzip | tar -xvf - names.dmp nodes.dmp
