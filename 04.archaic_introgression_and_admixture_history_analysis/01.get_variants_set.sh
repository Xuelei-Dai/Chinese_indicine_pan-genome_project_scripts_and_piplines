#Aligned each partially phased assembly to the reference genome (ARS-UCD1.2)
Threads_Num=$1
Reference=$2
Assembly=$3
Sample_Prefix=$4
minimap2 --paf-no-hit -a -x asm5 --cs -r2k -t ${Threads_Num} ${Reference} ${Assembly} | samtools sort -@ ${Threads_Num} -o ${Sample_Prefix}.sort.bam -
samtools index ${Sample_Prefix}.sort.bam

#SNV calling for Hap1 and Hap2
Reference=$1
SampleName=$2
Threads=$3
bcftools mpileup -O b -f ${Reference} -Q 20 -q 20 --annotate FORMAT/AD,FORMAT/DP --threads ${Threads} ${SampleName}_Hap1.sort.bam | bcftools call -m -v -O z -o ${SampleName}_Hap1.vcf.gz -

Reference=$1
SampleName=$2
Threads=$3
bcftools mpileup -O b -f ${Reference} -Q 20 -q 20 --annotate FORMAT/AD,FORMAT/DP --threads ${Threads} ${SampleName}_Hap2.sort.bam | bcftools call -m -v -O z -o ${SampleName}_Hap2.vcf.gz -

#Filter Hap VCF
for i in $(cat Sample.list)
do
mkdir -p $i && cd $i
for Hap in {1..2}
	do
	bash ../Filter_Hap_VCF.sh  ${i}_Hap${Hap}.vcf.gz ${i}_Hap${Hap}.filter.vcf.gz
	done
cd ..
done

###Short-read data mapping and variants calling
#QC for short-read data
Fastq1=$1
Fastq2=$2
SampleName=$3
Threads=$4
fastp -i ${Fastq1} -I ${Fastq2} -o ${SampleName}_1.clean.fastq.gz -O ${SampleName}_2.clean.fastq.gz --thread ${Threads}

#Build index for reference genome
bwa index ARS-UCD1.2_ChangeNamegenome.Chromosome.fasta
samtools faidx ARS-UCD1.2_ChangeNamegenome.Chromosome.fasta
java -jar picard.jar CreateSequenceDictionary R=ARS-UCD1.2_ChangeNamegenome.Chromosome.fasta O=ARS-UCD1.2_ChangeNamegenome.Chromosome.dict

#Passed quality-filtered reads were aligned to the reference genome
Reference=$1
Reads1=$2
Reads2=$3
SampleName=$4
Threads=$5
bwa mem -t ${Threads} -M -R "@RG\tID:${SampleName}\tLB:${SampleName}\tPL:ILLUMINA\tSM:${SampleName}" ${Reference} \
${Reads1} ${Reads2} | samtools view -bS - > ${SampleName}.bam
samtools sort ${SampleName}.bam -o ${SampleName}.sort.bam
samtools index ${SampleName}.sort.bam
rm ${SampleName}.bam

#Removing PCR deduplicates
SampleName=$1
java -Xmx10g -Djava.io.tmpdir=temp -jar picard.jar MarkDuplicates I=${SampleName}.sort.bam O=${SampleName}.dedup.sort.bam M=${SampleName}.dedup.txt REMOVE_DUPLICATES=true CREATE_INDEX=true ASSUME_SORTED=true VALIDATION_STRINGENCY=LENIENT MAX_FILE_HANDLES=2000

#SNP calling for short-read data
#Get GVCF
SampleName=$1
ChromName=$2
gatk \
	--java-options "-Xmx10g" \
	HaplotypeCaller \
	-ERC GVCF \
	-L ${ChromName} \
	-R ARS-UCD1.2_ChangeNamegenome.Chromosome.fasta \
	--minimum-mapping-quality 25 --base-quality-score-threshold 20 \
	-I ${SampleName}.dedup.sort.bam \
	-O ${SampleName}_${ChromName}.gvcf.gz

#Merge GVCF
Reference=$1
GVCF_List=$2
GVCF_SampleList_Prefix=$3
gatk \
	--java-options "-Xmx10g -Xms4g" \
	CombineGVCFs \
	--tmp-dir ./temp \
	-R ${Reference} \
        --variant ${GVCF_List} \
	-O ${GVCF_SampleList_Prefix}_merge.gvcf.gz

#Genotyping
Reference=$1
MergeGVCF=$2
Genotype_Prefix=$3
gatk \
	--java-options "-Xmx10g" \
	GenotypeGVCFs \
	--tmp-dir ./temp \
	-R ${Reference} \
	-V ${MergeGVCF} \
	-O ${Genotype_Prefix}.Genotype.vcf.gz

#Filter short-reads SNP
bcftools index cattle_NGS.Genotype.vcf.gz
bcftools view cattle_NGS.Genotype.vcf.gz -i 'MAF>0.01 & F_MISSING<=0.1' -v snps -M2 -m2 -O z -o cattle_NGS.Genotype.filter.vcf.gz
bcftools index cattle_NGS.Genotype.filter.vcf.gz

#Phasing short-reads SNP
java -Xmx20g -jar beagle.18May20.d20.jar \
	gt=cattle_NGS.Genotype.filter.vcf.gz \
	nthreads=20 \
	out=cattle_NGS.Genotype.filter.phase
bcftools index cattle_NGS.sample.Genotype.filter.phase.vcf.gz --threads 5


#Merge the SNVs of the Hap  and the SNPs of an individual(CL100006972_L01) in the short-read

bcftools view cattle_NGS.sample.Genotype.filter.phase.vcf.gz -s CL100006972_L01 -O z -o cattle_NGS.CL100006972_L01.Genotype.filter.phase.vcf.gz

mkdir -p TMP_File && cd TMP_File
mkdir -p log
for Sample in $(cat ../Sample.list)
do
bash ../script/Merge_SampleHap_SourceSample.sh ${Sample}_Hap1.filter.vcf.gz ${Sample}_Hap2.filter.vcf.gz cattle_NGS.CL100006972_L01.Genotype.filter.phase.vcf.gz Merge_${Sample}_Hap1_Hap2_CL100006972_L01.phase.vcf.gz
done

#Filter the merged VCF files and only keep the positions in the short-read VCF files
less cattle_NGS.sample.Genotype.filter.phase.vcf.gz | grep -v '#' |cut -f1,2 > genetic_map.position.txt

mkdir -p TMP_File && cd TMP_File
mkdir -p log
for Sample in $(cat ../Sample.list)
do
bash ../script/Filter_VCF_Position.sh Merge_${Sample}_Hap1_Hap2_CL100006972_L01.phase.vcf.gz ../genetic_map.position.txt ${Sample}
done

#Filter merged VCF
mkdir -p TMP_File && cd TMP_File
mkdir -p log
for Sample in $(cat ../Sample.list)
do
bash ../script/FilterMergeHapVCF.sh ${Sample}.Filter_Position.phase.recode.vcf.gz ${Sample}.Filter_Position.phase.recode.filter.vcf.gz
done

#Get the VCF of the Hap individual
mkdir -p TMP_File && cd TMP_File
mkdir -p log
for Sample in $(cat ../Sample.list)
do
python3 ../script/FillMergeHapVCF.py -v ${Sample}.Filter_Position.phase.recode.filter.vcf.gz -o ${Sample}.final.phase.vcf
bgzip ${Sample}.final.phase.vcf
bcftools index ${Sample}.final.phase.vcf.gz
done

#Merge the VCF of all Hap individuals
mkdir -p TMP_File && cd TMP_File
bcftools merge ./*.final.phase.vcf.gz -O z -o Chinese_indicine_MergeHap.vcf.gz

#Filer merged VCF of all Hap individuals
kdir -p TMP_File && cd TMP_File
bash ../script/Final_Filter.sh Chinese_indicine_MergeHap.vcf.gz Chinese_indicine_MergeHap.filter.vcf.gz


#Merge VCF of Hap and short-reads
bcftools merge Chinese_indicine_MergeHap.filter.vcf.gz cattle_NGS.sample.Genotype.filter.phase.vcf.gz -Oz -o cattle_final.Genotype.filter.phase.vcf.gz
bcftools index ${outvcf}
