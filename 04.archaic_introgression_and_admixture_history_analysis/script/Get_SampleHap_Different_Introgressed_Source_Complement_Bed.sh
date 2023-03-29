mkdir -p TMP_Bed
for SampleHap in $(cat SampleHap.list)
do
	for Source in $(cat Source.list)
	do
	bedtools complement -i TMP_Bed/${SampleHap}_${Source}_Source_Introgressed_Fragment.sort.bed -g ARS-UCD1.2_ChangeNamegenome.Chromosome.fasta.size > TMP_Bed/${SampleHap}_${Source}_Source_Introgressed_Fragment.sort.complement.bed
	done
done
