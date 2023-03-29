#Get Snp Counts From Bam
#genotype.allele.input is from SNP.vcf file, contain four columns:SNP's chr, position, ref allele, alt allele
#${sample}.keep.merge.sort.rmdup.final.bam is bamfile after mapping bias correction.
mkdir -p ../GetSnpCountFromBam_result
python3 ./script/GetSnpCountFromBam.py -s ../genotype.allele.input -b ../${sample}.keep.merge.sort.rmdup.final.bam -o ../GetSnpCountFromBam_result/${sample}_ASE1.o
bash ./script/cat_merge_ASEsample.sh

#filter:at least 3 samples, at least 20 total reads
python3 ./script/filter_sample3_reads20_mod.py -l ../GetSnpCountFromBam_result/ASE1_o_merge_result -o ../sample3_reads20_filter4_result

#get snpReads and snpGenotype intersect
#SNPs.filtered.vcf.gz is SNP's VCF file after filtered
bcftools query -f '%CHROM\t%POS\t%REF\t%ALT[\t%GT]\n' ../SNPs.filtered.vcf.gz >> ../SNPs.filtered.GT.vcf.gz
less ../SNPs.filtered.GT.vcf.gz| sed -e 's/0\/0/0/g' -e 's/0\/1/0.5/g' -e 's/1\/1/1/g' -e 's/.\/./2/g' >> ../SNPs.filtered.GT.txt
python3 ./scirpt/snpReads_snpGenotype_intersect.py -g ../SNPs.filtered.GT.txt -r ../sample3_reads20_filter4_result -o ../snpReads_snpGenotype_intersect.result

#FDR stastics
mkdir -p ../FDR & cd ../FDR
bash ./script/prepare_fdr.sh
bash ./script/fdr2.sh
bash ./script/merge3.sh
bash ./script/paste4.sh

#judge ASEsnp by ratio and FDR
python3 ./script/judge_ASEsnp.py -i ../snpReads_snpGenotype_intersect.result -o ../judge_ASEsnp.result
python3 ./script/judge_real_ASEsnp_byFDR.py -a ../judge_ASEsnp.result -f ../FDR/ASE_fdr_merge_result -o ../judge_real_ASEsnp_byFDR.result

##annotation of ASEsnp
#ANNOVAR,${annovar_PATH} is your ANNOVAR software path
#please replace "NA" by "0" in ../judge_real_ASEsnp_byFDR.result
#ASE_index_for_annot.info contain:SNP's chr, position, ref allele, alt allele. Produced by ../judge_real_ASEsnp_byFDR.result
mkdir -p ../annotation & cd ../annotation
${annovar_PATH}/annotate_variation.pl -out Anno.out -build ARS-UCD1.2_addnovel ASE_index_for_annot.info ${annovar_PATH}/ARS-UCD1.2_addnovel_db/
less ../annotation/Anno.out.variant_function |awk -v FS='\t' -v OFS='\t' '{print $3,$4,$5,$6,$7,$1,$2}' > ../annotation/Anno.out.variant_function_rerank
python3 ./script/getASEsnpAnnotion.py -i ../judge_real_ASEsnp_byFDR.result -a ../annotation/Anno.out.variant_function_rerank -o ../getASEsnpAnnotion.result
python3 ./script/judge_ASEgene_byASEsnp.py -a ../getASEsnpAnnotion.result -o ../judge_ASEgene_byASEsnp.result

#get the SV which located 100 kb upstream or downstream of the ASEgene
#bedtools_intersect_Gene_sv.+-100kb.result contain SV's annotation file and genotype infomation ${SV_position+-100kb_genotype_file}, please have this file ready
#The format of each line of the bedtools_intersect_Gene_sv.+-100kb.result is:
#chr SV_start SV_end SV_ID length ${sample_genotypes} annotation_chr annotation_gene_start annotation_gene_end annotation_gene_name
#note:The sample order of ${sample_genotypes} must be consistent with the sample order in the SNP.vcf file, SV.info is the SV's chr,position,ref,alt produced from SV.vcf.gz
mkdir -p ../annotation_sv & cd ../annotation_sv
${annovar_PATH}/annotate_variation.pl -out Anno.out -build ARS-UCD1.2 SV.info ${annovar_PATH}/ARS-UCD1.2_db/
bedtools intersect -a ${SV_position+-100kb_genotype_file} -b ${gene_position_file} -wa -wb > bedtools_intersect_Gene_sv.+-100kb.result
python3 ./script/AddGenotypeAseGene2annotion.py -i bedtools_intersect_Gene_sv.+-100kb.result -a ../judge_ASEgene_byASEsnp.result -n ../annotation_sv/Anno.out.variant_function -o ../AddGenotypeAseGene2annotion.result
python3 ./script/filterSVgenotype0-1dayu3.py -a ../AddGenotypeAseGene2annotion.result -o ../filterSVgenotype0-1dayu3.result

#get ASEgene SV pairs
python3 ./script/getASEgene_sv_pair.py -a ../filterSVgenotype0-1dayu3.result -o ../getASEgene_sv_pair.result
cat ../getASEgene_sv_pair.result |awk '{print $1"\t"$2"\t"$3"\t"$4"\t"$5"\t"$25"\t"$26"\t"$27"\t"$28"\t"$48"\t"$49}' > ../SV_Asegene_Annotation.pair.result



