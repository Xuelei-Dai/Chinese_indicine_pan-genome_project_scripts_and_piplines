#Split all sample introgressed fragment
mkdir -p Split_SampleHap_Introgression_Fragments_Bed
for Sample in $(cat Sample.list)
do
less All_Sample_Introgressed_Fragment.csv | awk '{if($9=="'${Sample}'" && $5=="hap1") print $1"\t"$2"\t"$3"\t""'${Sample}'""_Hap1"}' > Split_SampleHap_Introgression_Fragments_Bed/${Sample}_Hap1_Introgressed_Fragment.bed
less All_Sample_Introgressed_Fragment.csv | awk '{if($9=="'${Sample}'" && $5=="hap2") print $1"\t"$2"\t"$3"\t""'${Sample}'""_Hap2"}' > Split_SampleHap_Introgression_Fragments_Bed/${Sample}_Hap2_Introgressed_Fragment.bed
done

#Extract the sequence of the region where the introgressed fragment is located
mkdir -p Introgression_Sample_Hap_Seq && cd Introgression_Sample_Hap_Seq
for Sample in $(cat ../Sample.list)
do
python3 ../script/GetSampleHaplotypeSeqFromPhaseVcf.py -v ../cattle_final.Genotype.filter.phase_Add_Kouprey.vcf.gz -b ../Split_SampleHap_Introgression_Fragments_Bed/${Sample}_Hap1_Introgressed_Fragment.bed -o ${Sample}_Hap1
python3 ../script/GetSampleHaplotypeSeqFromPhaseVcf.py -v ../cattle_final.Genotype.filter.phase_Add_Kouprey.vcf.gz -b ../Split_SampleHap_Introgression_Fragments_Bed/${Sample}_Hap2_Introgressed_Fragment.bed -o ${Sample}_Hap2
done

#Get the sequence of the introgressed region corresponding to the control individual
mkdir -p Split_SampleHap_Introgression_Fragments_Bed
for Sample in $(cat Sample.list)
do
less Split_SampleHap_Introgression_Fragments_Bed/${Sample}_Hap1_Introgressed_Fragment.bed | awk '{print $1":"$2"-"$3}' > Split_SampleHap_Introgression_Fragments_Bed/${Sample}_Hap1_Introgressed_Fragment.Region.list
less Split_SampleHap_Introgression_Fragments_Bed/${Sample}_Hap2_Introgressed_Fragment.bed | awk '{print $1":"$2"-"$3}' > Split_SampleHap_Introgression_Fragments_Bed/${Sample}_Hap2_Introgressed_Fragment.Region.list
done

mkdir -p Ref_Sample_Seq && cd Ref_Sample_Seq
for Sample in $(cat ../Sample.list)
do
python3 ../script/Get_Ref_Sample_Seq_VCF2IUPACGT.py -v ../cattle_final.Genotype.filter.phase_Add_Kouprey.vcf.gz -s ../Ref_Sample.list -r ../Split_SampleHap_Introgression_Fragments_Bed/${Sample}_Hap1_Introgressed_Fragment.Region.list -m ../Ref_Sample.MapSpecies.list -o ${Sample}_Hap1
python3 ../script/Get_Ref_Sample_Seq_VCF2IUPACGT.py -v ../cattle_final.Genotype.filter.phase_Add_Kouprey.vcf.gz -s ../Ref_Sample.list -r ../Split_SampleHap_Introgression_Fragments_Bed/${Sample}_Hap2_Introgressed_Fragment.Region.list -m ../Ref_Sample.MapSpecies.list -o ${Sample}_Hap2
done

#Merge sequence of target and control individuals introgressed regions
for Sample in $(cat AsianIndicus.sample.list)
do
bash ./script/Merge_Introgression_Ref_Seq.sh ${Sample}_Hap1
bash ./script/Merge_Introgression_Ref_Seq.sh ${Sample}_Hap2
done

#Construct ML trees using MEGA
mkdir -p ML_result
for Sample in $(cat ../Sample.list)
do
python3 ./script/IntrogressionFragment2MEGA_ML.py -b Split_SampleHap_Introgression_Fragments_Bed/${Sample}_Hap1_Introgressed_Fragment.Region.list -r /path/outgroup.txt -s ${Sample}_Hap1 -q jynodequeue -t 1 -m 10
python3 ./script/IntrogressionFragment2MEGA_ML.py -b Split_SampleHap_Introgression_Fragments_Bed/${Sample}_Hap2_Introgressed_Fragment.Region.list -r /path/outgroup.txt -s ${Sample}_Hap2 -q jynodequeue -t 1 -m 10
done

#Merge all introgressed fragments branchLength tree file
for Sample in $(cat AsianIndicus.sample.list)
do
ls ./ML_result/${Sample}_Hap1/*.nwk | grep -v 'consensus' >> All_Sample_BranchLength_Tree.nwk
ls ./ML_result/${Sample}_Hap2/*.nwk | grep -v 'consensus' >> All_Sample_BranchLength_Tree.nwk
done

#Add lable to merged branchLength tree file
python3 ./script/MergeBranchLengthTree.py -t All_Sample_BranchLength_Tree.nwk  -o Merge_BranchLength_Tree.nwk

#Determining the source of introgressed fragments
python3 ./script/IntrogressionFragmentSourceClassifyFromPhylogeneticTree.py -t All_Sample_BranchLength_Tree.nwk -r Buffalo_SRR12452300 -o All_Sample_Introgressed_Fragment.Source




