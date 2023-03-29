#More detail information can be found in github.com/bmvdgeijn/WASP/
#Split SNP's VCF for each chromosome
#chr.list contain the name of the chromosome;
#SNPs.filtered.vcf.gz is the SNP's genotyping VCF file.
mkdir -p ../SNP_vcf
cd ../SNP_vcf
for chrID in $(cat ../chr.list)
do
bcftools view -r ${chrID} SNPs.filtered.vcf.gz -o chr${chrID}.vcf.gz -O z
done
#Creating text based SNP files
bash ./script/extract_vcf_snps.sh ../SNP_vcf/ ../output_snp_dir/

#Use find_intersecting_snps.py to identify reads that may have mapping biases
#sample.txt contain the name of samples
#${sample}.sort.bam:Coordinate-sorted input BAM file containing mapped reads
python3 ./script/find_intersecting_snps.py --is_paired_end --is_sorted --output_dir ../intersecting_output --snp_dir ../output_snp_dir --samples sample.txt map1/${sample}.sort.bam

#Map the PREFIX.remap.fq.gz using same mapping software (STAR)
STAR --genomeDir $INDEX --readFilesIn ../intersecting_output/${sample}.remap.fq1.gz ../intersecting_output/${sample}.remap.fq2.gz --readFilesCommand zcat --runThreadN 8 --outFilterIntronMotifs RemoveNoncanonical Unannotated --outFilterMismatchNmax 10 --outFilterMultimapNmax 1 --outSAMstrandField intronMotif --outSJfilterReads Unique --outSAMtype BAM SortedByCoordinate --outReadsUnmapped Fastx --outFileNamePrefix ../map2/${sample}

#filter remapped reads
python3 ./script/filter_remapped_reads.py  ../intersecting_output/${sample}.to.remap.bam ../map2/${sample}Aligned.sortedByCoord.out.bam ../filter_remapped_reads_output/${sample}.keep.bam

#merge bam
samtools merge ../${sample}.keep.merge.bam ../filter_remapped_reads_output/${sample}.keep.bam ../intersecting_output/${sample}.keep.bam
samtools sort -o ../${sample}.keep.merge.sort.bam ../${sample}.keep.merge.bam
samtools index ../${sample}.keep.merge.sort.bam

#remove duplication reads of bam
python3 ./script/rmdup_pe.py ../${sample}.keep.merge.sort.bam ../${sample}.keep.merge.sort.rmdup.bam

#index and sort
samtools sort -o ../${sample}.keep.merge.sort.rmdup.final.bam ../${sample}.keep.merge.sort.rmdup.bam
samtools index ../${sample}.keep.merge.sort.rmdup.final.bam
