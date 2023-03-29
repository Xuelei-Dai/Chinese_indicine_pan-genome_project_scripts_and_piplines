#Calculated the fixation index (Fst) of SVs between Chinese indicine cattle and Indian indicine cattle using VCFtools
vcftools --gzvcf Merge_DEL_INS.genotypes.filter.sort.vcf.gz --weir-fst-pop Chinese_indicine.sample.list --weir-fst-pop Indian_indicine.sample.list --out Chinese_indicine.Indian_indicine --max-missing 0.1 --maf 0.01

#permutation tests 1000 times to calculate the empirical p-values for the result of Fst. Refer to https://github.com/uod12345/fst-permutation-tests
bash ./script/run_permutation_test.sh Merge_DEL_INS.genotypes.filter.sort.vcf.gz ./ Chinese_indicine.sample.list Indian_indicine.sample.list 1000 100  10

#Call SVs for two partially phased assemblies of each Chinese indicine cattle using SVIM-asm
for SampleName in $(cat Sample.list)
do
	mkdir -p ${SampleName}_Hap1 && cd ${SampleName}_Hap1
	bash ../script/SVIM-asm.sh ~/cattle/data/Refrence.genome/ARS-UCD1.2_ChangeNamegenome.Chromosome.fasta ${SampleName} ${SampleName}_Hap1
	cd ..
done

for SampleName in $(cat Sample.list)
do
        mkdir -p ${SampleName}_Hap2 && cd ${SampleName}_Hap2
        bash ../script/SVIM-asm.sh ~/cattle/data/Refrence.genome/ARS-UCD1.2_ChangeNamegenome.Chromosome.fasta ${SampleName} ${SampleName}_Hap2
        cd ..
done

#Change format of VCF file 
for SampleName in $(cat Sample.list)
do
	cd ${SampleName}_Hap1
	python3 ../script/Change_SVIM_asm_VCF_Format.py -v variants.vcf -o ${SampleName}_Hap1.ChangeFormat.vcf 
	cd ..
done

for SampleName in $(cat Sample.list)
do
        cd ${SampleName}_Hap2
        python3 ../script/Change_SVIM_asm_VCF_Format.py -v variants.vcf -o ${SampleName}_Hap2.ChangeFormat.vcf
        cd ..
done

#Change the format of read-based SV set
python3 ./script/Change_SV_VCF_Format.py -v Merge_DEL_INS.genotypes.filter.sort.vcf -o Merge_DEL_INS.genotypes.filter.sort.ChangeFormat.vcf

#Merge the SV of each partially phase assembly with read-based SV using the SURVIVOR software
for SampleName in $(cat Sample.list)
do
	cd ${SampleName}_Hap1
	echo "./${SampleName}_Hap1/${SampleName}_Hap1.ChangeFormat.vcf" >> ${SampleName}_Hap1.merge_vcf_files_raw_calls.txt
	echo "./Merge_DEL_INS.genotypes.filter.sort.ChangeFormat.vcf" >> ${SampleName}_Hap1.merge_vcf_files_raw_calls.txt
	cd ..
done

for SampleName in $(cat Sample.list)
do
        cd ${SampleName}_Hap2
        echo "./${SampleName}_Hap2/${SampleName}_Hap2.ChangeFormat.vcf" >> ${SampleName}_Hap2.merge_vcf_files_raw_calls.txt
        echo "./Merge_DEL_INS.genotypes.filter.sort.ChangeFormat.vcf" >> ${SampleName}_Hap2.merge_vcf_files_raw_calls.txt
        cd ..
done

for SampleName in $(cat Sample.list)
do
	cd  ${SampleName}_Hap1
	 SURVIVOR merge ${SampleName}_Hap1.merge_vcf_files_raw_calls.txt 10 2 1 0 0 50 ${SampleName}_Hap1.merged.vcf
	cd ..
done

for SampleName in $(cat Sample.list)
do
        cd  ${SampleName}_Hap2
         SURVIVOR merge ${SampleName}_Hap2.merge_vcf_files_raw_calls.txt 10 2 1 0 0 50 ${SampleName}_Hap2.merged.vcf
        cd ..
done

#identify the common SV is located on each partially phase assemblies SV
for SampleName in $(cat Sample.list)
do
	cd ${SampleName}_Hap1
	python3 ../script/Get_SV_On_Sample_Haplotyp.py -v ${SampleName}_Hap1.merged.vcf -s ${SampleName}_Hap1 -o ${SampleName}_Hap1_SVID.list 
	cd ..
done

for SampleName in $(cat Sample.list)
do
        cd ${SampleName}_Hap2
        python3 ../script/Get_SV_On_Sample_Haplotyp.py -v ${SampleName}_Hap2.merged.vcf -s ${SampleName}_Hap2 -o ${SampleName}_Hap2_SVID.list
	cd ..
done

#Merge the common SV is located on each partially phase assemblies SV
for SampleName in $(cat Sample.list)
do
	cd ${SampleName}_Hap1
	cat ${SampleName}_Hap1_SVID.list | grep -v '#' | awk '{print "'${SampleName}'""_Hap1|"$1}' >> ../All_Sample_Hap_SV.list
	cd ..
done

for SampleName in $(cat Sample.list)
do
        cd ${SampleName}_Hap2
        cat ${SampleName}_Hap2_SVID.list | grep -v '#' | awk '{print "'${SampleName}'""_Hap2|"$1}' >> ../All_Sample_Hap_SV.list
	cd ..
done

#Get the archaic introgressed fragments bed file (the result of “Identifying archaic introgressed fragments” section)
less All_Sample_Final_Introgressed_Fragment.Source.csv | grep -v 'Source' |cut -f3,4,5,9 > All_Sample_Hap_Final_Introgressed_Fragment.bed

python3 ./cript/Get_Sample_Hap_SV_ID_Bed.py -v Merge_DEL_INS.genotypes.filter.sort.ChangeFormat.vcf -s All_Sample_Hap_SV.list -o All_Sample_Hap_SV.bed

#Get the SV fall on the archaic introgressed fragments
bedtools intersect -a All_Sample_Hap_Final_Introgressed_Fragment.bed -b All_Sample_Hap_SV.bed -wa -wb |awk '{if($4==$9) print $0}' > All_Sample_Hap_SV_On_Introgressed_Fragment.bed

#Get final introgressed SVs
less All_Sample_Hap_SV_On_Introgressed_Fragment.bed |cut -f8 |sort |uniq > All_Sample_Hap_Uniq_SV_On_Introgressed_Fragment.list
cat All_Sample_Hap_Uniq_SV_On_Introgressed_Fragment.list Merge.Chinese_indicine_DEL_INS_with_wild_Bos_Shared.SV.list |sort |uniq -c | awk '{if($1==2) print $2}' > Final_Introgressed_SV.list

#Get Chinese indicine cattle candidate population-stratified SVs
less CHI_fst_add_pvalues.final.tsv |grep -v 'chrom' | awk '{if($5< 0.05 && $4 >0.1) print $3}' > Chinese_indicine_population_stratified_SV.list

#Get the intersection of population-stratified and introgressed SVs of Chinese indicine cattle
cat Final_Introgressed_SV.list Chinese_indicine_population_stratified_SV.list |sort |uniq -c | awk '{if($1==2) print $2}' > Chinese_indicine_population_stratified_Introgressed_SV.list
