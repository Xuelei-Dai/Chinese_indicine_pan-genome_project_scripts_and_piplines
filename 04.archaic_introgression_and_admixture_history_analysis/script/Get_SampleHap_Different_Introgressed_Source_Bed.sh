mkdir -p TMP_Bed
for SampleHap in $(cat SampleHap.list)
do
	for Source in $(cat Source.list)
	do
	less All_Sample_Introgressed_Fragment.Source | grep "${SampleHap}" | grep "${Source}" | cut -f1 | sed 's/:/\t/g' | sed 's/-/\t/g' | sed 's/_/\t/g' | awk '{print $1"\t"$2"\t"$3}' | bedtools sort -g ARS-UCD1.2_ChangeNamegenome.Chromosome.fasta.size -i - > TMP_Bed/${SampleHap}_${Source}_Source_Introgressed_Fragment.sort.bed
	done
done
