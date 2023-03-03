mkdir -p TMP_Bed
for SampleHap in $(cat SampleHap.list)
do
	for Source in $(cat Source.list)
	do
	cat  TMP_Bed/${SampleHap}_${Source}_Source_Fragmet_Length >> TMP_Bed/${Source}_Source_Fragmet_Length
	done
done
