#Create a spliced pangenome graph and indexes
vg autoindex --workflow mpmap -t 4 --prefix vg_rna --ref-fasta ARS.fa --vcf cattle_genotyping.vcf.gz --tx-gff GCF_002263795.1_ARS-UCD1.2_genomic.ChangeChromName.Chromosome.gtf
#RNA-seq reads can be mapped to the spliced pangenome graph using vg mpmap
vg mpmap -n rna -t 4 -x vg_rna.spliced.xg -g vg_rna.spliced.gcsa -d vg_rna.spliced.dist -f data/ERR789826_1.clean.fq.gz -f data/ERR789826_2.clean.fq.gz > mpmap.gamp

