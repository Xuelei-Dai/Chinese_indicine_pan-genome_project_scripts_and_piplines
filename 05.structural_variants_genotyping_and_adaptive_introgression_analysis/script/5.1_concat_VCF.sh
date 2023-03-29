VCF_List=$1
OUT_VCF_Prefix=$2
bcftools concat -f ${VCF_List} -O z -o ${OUT_VCF_Prefix}.genotypes.vcf.gz
tabix ${OUT_VCF_Prefix}.genotypes.vcf.gz
