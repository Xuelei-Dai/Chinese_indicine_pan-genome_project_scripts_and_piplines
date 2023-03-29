mkdir -p TMP_Bed
for SampleHap in $(cat SampleHap.list)
do
	for Source in $(cat Source.list)
	do
	less TMP_Bed/${SampleHap}_${Source}_Source_Introgressed_Fragment.sort.bed | grep -v 'X' | awk '{print ($2/100000000)"\t"($3/100000000)"\t""0"}' > TMP_Bed/${SampleHap}_${Source}_Source_Introgressed_Fragmet_Length
	less TMP_Bed/${SampleHap}_${Source}_Source_Introgressed_Fragment.sort.complement.bed | grep -v 'X' | awk '{print ($2/100000000)"\t"($3/100000000)"\t""1"}' > TMP_Bed/${SampleHap}_${Source}_Source_Introgressed_Fragmet_complement_Length
	cat TMP_Bed/${SampleHap}_${Source}_Source_Introgressed_Fragmet_Length TMP_Bed/${SampleHap}_${Source}_Source_Introgressed_Fragmet_complement_Length > TMP_Bed/${SampleHap}_${Source}_Source_Fragmet_Length
	done
done
