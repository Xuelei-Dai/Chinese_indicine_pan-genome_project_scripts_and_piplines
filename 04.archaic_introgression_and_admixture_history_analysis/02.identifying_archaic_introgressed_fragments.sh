#Introgression detection,please refer to the https://pypi.org/project/hmmix/ page
#Prepare individuals File(individuals.json)

##Prepare weights.bed
less ARS-UCD1.2_ChangeNamegenome.Chromosome.fasta.fai |awk '{print $1"\t""1""\t"$2}' > ARS-UCD1.2_weights.bed

#Prepare Ancenstor Site File
python3 ./script/BuffaloGenomeMap2ARS-UCD1.2.py -v cattle_final.Genotype.filter.phase.vcf.gz -g ARS-UCD1.2_ChangeNamegenome.Chromosome.fasta -s SRR12452300 -o Taurine_Indicine_ancestor.fa

#Finding snps which are derived in the outgroup
bash ./script/create_outgroup.sh

#Estimating mutation rate across genome (We can use the number of variants in the outgroup to estimate the substitution rate as a proxy for mutation rate.)
sh ./script/mutation_rate.sh

#Find a set of variants which are not derived in the outgroup
sh /script/create_ingroup.sh

#Training
for Sample in $(cat Sample.list)
do
bash ./script/Training.sh ${Sample}
done

#Decode and Annotate with known admixing population
for Sample in $(cat Sample.list)
do
bash ./script/Decode.sh ${Sample}
done

#Merge all sample introgressed fragment
for Sample in $(cat Sample.list)
do
less ${Sample}.Decode.txt | grep -v '-' | grep -v '>' | grep 'Archaic' | grep 'hap' |sed 's/_/\t/g' | awk '{if($7>0.9 && $3!=$4) print $1"\t"$3"\t"$4"\t"$5"\t"$2"\t"$6"\t"$7"\t"$8"\t""'${Sample}'"}' >> All_Sample_Introgressed_Fragment.csv
done
sed -i '1i\Chrom\tStart\tEnd\tLength\tHap\tSource\tMean_Prob\tSNP_Num\tSample' All_Sample_Introgressed_Fragment.csv
