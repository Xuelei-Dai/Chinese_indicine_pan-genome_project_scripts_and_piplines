IN_VCF=$1
VCF_Prefix=`basename ${IN_VCF} .vcf.gz`

bcftools index ${IN_VCF}
bcftools view ${IN_VCF} -i 'MAF>0.01 & F_MISSING<=0.1' -O z -o ${VCF_Prefix}.filter.vcf.gz
