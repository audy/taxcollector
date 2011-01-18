require 'rake/clean'

task :default => 'tc_rdp.fa' do
  
end

task :ncbi => ['names.dmp', 'nodes.dmp']
task :rdp => 'rdp.fa'

file 'tc_rdp.fa' => ['rdp.fa', 'names.dmp', 'nodes.dmp'] do
  sh 'python taxcollector.py names.dmp nodes.dmp rdp.fa > tc_rdp.fa'  
end

file 'names.dmp', 'nodes.dmp' do |task|
  url = 'ftp://ftp.ncbi.nih.gov/pub/taxonomy/taxdump.tar.gz'
  sh "curl #{url} | gunzip | tar -xvf - names.dmp nodes.dmp" do |okay, res|
    if not okay
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