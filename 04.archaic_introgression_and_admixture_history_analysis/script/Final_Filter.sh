IN_VCF=$1
OUT_VCF=$2
bcftools index ${IN_VCF}
bcftools view ${IN_VCF} -i 'F_MISSING<=0' -O z -o ${OUT_VCF}
bcftools index ${OUT_VCF}
