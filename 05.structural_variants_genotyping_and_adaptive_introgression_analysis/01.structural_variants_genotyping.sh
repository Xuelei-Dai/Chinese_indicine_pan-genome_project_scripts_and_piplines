#Get Bam depth
mkdir -p ../BamStat_SampleManifest
cd ../BamStat_SampleManifest
for i in $(cat ../final.sample.list)
do
ln -s ./BamStat_SampleManifest/${i}.txt
bash ../script/1.GetBamDepth.sh ARS-UCD1.2_ChangeNamegenome.Chromosome.fasta $i.dedup.sort.bam 4
done

#Split SV's VCF for each chromosome
sh ../script/2.Get_ChromVCF.sh Total_sample.merged.FinalIntegrated.filter.sort.vcf DEL_INS

#SV genotyping
mkdir -p ../DEL_INS_results && cd ../DEL_INS_results
for SampleName in $(cat ../final.sample.list)
do
mkdir -p ${SampleName} && cd ${SampleName}
for ChromName in {1..29} X
	do
		mkdir Chr_${ChromName} && cd Chr_${ChromName}
		bash ../script/3.Paragraph_genotyping.sh ARS-UCD1.2_ChangeNamegenome.Chromosome.fasta ./DEL_INS.INPUT_VCF/Chr${ChromName}.vcf.gz ./BamStat_SampleManifest/${SampleName}.txt 1
		cd ..
	done
	cd ..
done

#Get SV genotyping individual VCF file
cd ../DEL_INS_results
for SampleName in $(cat ../final.sample.list)
do
cd ${SampleName}
for ChromName in {1..29} X
	do
		cd Chr_${ChromName}
		bcftools view ./${SampleName}/genotypes.vcf.gz -O z -o ./${SampleName}/${SampleName}.genotypes.vcf.gz -s ${SampleName}
		cd ..
	done
cd ..
done

#Concat VCF
cd ../DEL_INS_results
for SampleName in $(cat ../final.sample.list)
do
	cd ${SampleName}
	ls ./*/${SampleName}/${SampleName}.genotypes.vcf.gz > ${SampleName}.genotypes.vcf.list
	bash ../../script/5.1_concat_VCF.sh ${SampleName}.genotypes.vcf.list ${SampleName}
	cd ..
done

#Merge VCF
cd ../DEL_INS_results
ls ./*/*.genotypes.vcf.gz > genotypes.vcf.list
bash ../script/5.2_merge_VCF.sh genotypes.vcf.list Merge_DEL_INS.genotypes.vcf.gz

#Filter VCF
cd ../DEL_INS_results
bash ../script/6.Filter_VCF.sh Merge_DEL_INS.genotypes.vcf.gz
