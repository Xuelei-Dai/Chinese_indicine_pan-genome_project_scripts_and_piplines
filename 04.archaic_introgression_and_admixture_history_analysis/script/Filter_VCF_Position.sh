Merge_VCF=$1
Position_File=$2
OUT_VCF_Prefix=$3
vcftools --gzvcf ${Merge_VCF} --positions ${Position_File} --recode --out  ${OUT_VCF_Prefix}.Filter_Position.phase
bgzip ${OUT_VCF_Prefix}.Filter_Position.phase.recode.vcf
bcftools index ${OUT_VCF_Prefix}.Filter_Position.phase.recode.vcf.gz
