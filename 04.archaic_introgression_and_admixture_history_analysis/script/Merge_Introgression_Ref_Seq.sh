SampleHap=$1
mkdir -p Merge_Introgression_Ref_Seq && cd Merge_Introgression_Ref_Seq
mkdir ${SampleHap}

for Region in $(cat ../Split_SampleHap_Introgression_Fragments_Bed/${SampleHap}_Introgressed_Fragment.Region.list)
do
cat ../Ref_Sample_Seq/${SampleHap}/${Region}.fasta ../Introgression_Sample_Hap_Seq/${SampleHap}/${Region}.fasta > ${SampleHap}/${Region}.fasta
done
