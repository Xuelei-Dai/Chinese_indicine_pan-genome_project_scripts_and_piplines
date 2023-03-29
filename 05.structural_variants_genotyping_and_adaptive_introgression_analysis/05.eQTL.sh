#get Covariates
#Merge.DEL_INS.transcriptome_sample.vcf.gz is the SV's VCF file
vcftools --gzvcf Merge.DEL_INS.transcriptome_sample.vcf.gz --plink --out DEL_INS.transcriptome_sample --max-missing 0.9 --maf 0.05
plink --file DEL_INS.transcriptome_sample --pca --chr-set 30 --maf 0.05 --out DEL_INS.transcriptome_sample.PCA
cat DEL_INS.transcriptome_sample.PCA.eigenvec | awk '{print $2 "\t" $3 "\t" $4 "\t" $5}'| awk '{for(i=1;i<=NF;i++)a[NR,i]=$i}END{for(j=1;j<=NF;j++)for(k=1;k<=NR;k++)printf k==NR?a[k,j] RS:a[k,j] FS}'|sed 's/^/id /g' |sed 's/ /\t/g' > covariate.txt

#eQTL by fastQTL software
#${fastQTL_path} is the path of fastQTL software
#geneExpr_TPM.sort.bed.gz is the expression file of all gene
#more detail can be found in http://fastqtl.sourceforge.net/
${fastQTL_path}/fastQTL.static --vcf Merge.DEL_INS.transcriptome_sample.vcf.gz --bed geneExpr_TPM.sort.bed.gz --out nominals --commands 30 commands.29andX.txt --cov covariate.txt


