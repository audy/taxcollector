require 'rake/clean'

task :default => ['taxcollector.fa'] do
  puts "TaxCollector -> taxcollector.fa"
end

CLEAN.include('rdp_tc.fa', 'rdp_filtered.fa', 'rdp_tc.fa', 'taxcollector.fa')
CLOBBER.include('names.dmp', 'nodes.db', 'rdp.fa', )

task :ncbi => ['names.dmp', 'nodes.dmp']
task :rdp => 'rdp.fa'

# Running of Scripts

file 'rdp_tc.fa' => ['rdp.fa', 'names.dmp', 'nodes.dmp'] do
  sh 'python taxcollector.py names.dmp nodes.dmp rdp.fa > rdp_tc.fa' do |okay, res|
    unless okay
      rm 'taxcollector.fa'
      fail res
    end
  end
end

file 'taxcollector.fa' => 'rdp_tc.fa' do
  sh "python filter_and_remove_duplicates.py rdp_tc.fa > taxcollector.fa" do |okay, res|
    unless okay
      rm 'rdp_filtered.fa'
      fail res
    end
  end
end

# Fetching of Databases

file 'names.dmp', 'nodes.dmp' do |task|
  url = 'ftp://ftp.ncbi.nih.gov/pub/taxonomy/taxdump.tar.gz'
  sh "curl #{url} | gunzip | tar -xvf - names.dmp nodes.dmp" do |okay, res|
    unless okay
      rm 'names.dmp'
      rm 'nodes.dmp'
      fail res
    end
  end
end

file 'rdp.fa' do
  url = "http://rdp.cme.msu.edu/download/release10_24_unaligned.fa.gz"
  sh "curl #{url} | gunzip > rdp.fa" do |okay, res|
    unless okay
      rm 'rdp.fa'
      fail res
    end
  end
end