#This removes all non-top-level bubbles from the VCF, unless they are nested inside a top-level bubble with a reference length exceeding 100kb.
vcfbub -l 0 -r 100000 -i ../cattle.pg/cattle.pg.vcf.gz > cattle.pg.filter.vcf.gz
#This removes all records carrying a missing allele: “.” or “CONFLICT”.
cat cattle.pg.filter.vcf|awk '$10!=".|."'|awk '$10!=".|1"'|awk '$10!="1|."'|awk '$10!="2|2"'|grep -v "CONFLICT=" >cattle.pg.filter.rm.vcf
#Genotyping and phasing based on kmer-counting and known haplotype sequences.
PanGenie -i ../data/SRR12452240.fastq -r ../data/ARS.fa -v cattle.pg.filter.rm.vcf -o cattle
