# TaxCollector 1.5.0


* Austin G. Davis-Richardson 
  <harekrishna@gmail.com>

* Triplett Lab
  Department of Microbiology & Cell Science
  University of Florida, Gainesville, FL


# Description
  
These scripts can be used to derive full taxonomic descriptions from the FASTA
files of the Ribosomal Database Project () and GreenGenes () 16s rRNA sequence
databases.

Elaboration of the taxonomy allows for the files to be used later on in 
with NCBI Blast.

# Scripts
  
 * __greengenes.py__ - Taxonomic Elaborator for the GreenGenes database.
 * __rdp.py__ - Taxonomic Elaborator for the RDP database.
 * __acctotax.py__ - Generates a flat text file of ProkMSA numbers and their corresponding
   NCBI TaxIDs for use by Green.py
 * __common.py__ - Common subroutines used by `rdp.py` and `greengenes.py`
    
# Instructions

* __Taxonomy Files__:

  First download the taxdump file from NCBI (ftp://ftp.ncbi.nih.gov/pub/taxonomy/)
  and extract it.  You will need the `names.dmp` and `nodes.dmp` files.  It is a good
  idea to update these as often as you update the RDP/GreenGenes databases.

  You can do this with one command!
  `curl ftp://ftp.ncbi.nih.gov/pub/taxdump.tar.gz | gunzip | tar -xvf names.dmp nodes.dmp`

	This will download and extract `names.dmp` and `nodes.dmp`

* __RDP__:

	Download the RDP FASTA file from the Ribosomal Database Project.
	The script can be invoked thusly,

	`python rdp.py names.dmp nodes.dmp input_fasta_file.fas output_fasta_file.fas`
        
* __GreenGenes__:
      
  The GreenGenes database requires an extra step.  You must generate a table
  of corresponding ProkMSA ID's and TaxIDs.  To do this, download the Green-
  Genes database in "GreenGenes" format (usually a .txt file).  Then run the
  script acctotax to generate the table:

	You need to download and extract this file, which is `inputfile`:
	
	<http://greengenes.lbl.gov/Download/Sequence_Data/Greengenes_format/greengenes16SrRNAgenes.txt.gz>
   
	Then generate proktable.txt
       
  `python acctotax.py inputfile`
          
  The script automatically generates an output file named 'inputfileout'        
  Now you can run the TaxCollector script, green.py which is invoked as thus,
          
  `python green.py names.dmp nodes.dmp proktable.txt input.fas output.fas`

* __Removing Duplicates__:

	Sometimes it's useful to remove duplicate entires if you combine an RDP
	and GreenGenes database.  This can be acheived with `rempdup.py`
	
	`python remdup.py <fasta file 1> <fasta file 2> <output file>`
		
	This script removes duplicate FASTA files based on headers, not sequences.
	It also requires that you have more RAM than the size of your sequence files.
          
# Output Format
  
These scripts output headers in the following format:
    
    >[7]Domain[6]Phylum[5]Class[4]Order[3]Family[2]Genus[1]Species
    
Weird NCBI taxonomies are not included, such as "subphylum"
You can alter this by editing the global list TaxExemption
Note that order and case matter.
 
If there is a gap between levels of taxonomy in the NCBI names database, Tax-
Collector will repeat the lower level in quotes, example:
    
    >[7]Domain[6]Phylum[5]"Order"[4]Order[3]Family[2]Genus[1]Species
    