##Align PacBio HiFi reads to a reference genome(ARS-UCD1.2), the recommended aligner is pbmm2.
Reference_Fa=$1
HiFi_Fa=$2
Sample_prefix=$3
pbmm2 align ${Reference_Fa} ${HiFi_Fa} ${Sample_prefix}.sort.bam --sort --preset HiFi --sample ${Sample_prefix} --rg "@RG\tID:${Sample_prefix}"

##Using pbsv to call structural variants
#Discover signatures of structural variation
pbsv discover ${Sample_prefix}.sort.bam ${Sample_prefix}.svsig.gz
#Call structural variants and assign genotypes
pbsv call --ccs -m 50 ${Reference_Fa} ${Sample_prefix}.svsig.gz ${Sample_prefix}.vcf

##Using cuteSV to call structural variants
Sort_BAM=$1
Reference_Fa=$2
Sample_Prefix=$3
Threads=$4
cuteSV ${Sort_BAM} ${Reference_Fa} ${Sample_Prefix}.vcf ./ \
	--max_cluster_bias_INS 1000 \
	--diff_ratio_merging_INS 0.9 \
	--max_cluster_bias_DEL	1000 \
	--diff_ratio_merging_DEL 0.5 \
	--genotype --sample ${Sample_Prefix} --threads ${Threads} --min_mapq 20 --min_size 30 --max_size 100000

##Using SVIM to call structural variants
BAM=$1
Reference=$2
SampleName=`basename ${BAM} .sort.bam`
svim alignment ./ ${BAM} ${Reference} --min_mapq 20 --min_sv_size 30 --max_sv_size 100000 --minimum_depth 3 --sample ${SampleName} --sequence_alleles --insertion_sequences

##Using Sniffles to call structural variants
Ref=$1
BAM=$2
prefix=$3
#Add MD tag to BAM:
samtools calmd -bS ${BAM} ${Ref} > ${prefix}.add_md.sort.bam
#SV calling
sniffles -m ${prefix}.add_md.sort.bam --genotype -v ${prefix}.vcf -s 3 --report-seq --report_str --ccs_reads
