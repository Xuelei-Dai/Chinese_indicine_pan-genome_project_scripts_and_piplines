IN_VCF=$1
OUT_VCF=$2
bcftools view ${IN_VCF} -v snps -M2 -m2 -O z -o ${OUT_VCF}
