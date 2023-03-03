VCF_list=$1
OUT_VCF=$2
bcftools merge --file-list ${VCF_list} -O z -o ${OUT_VCF}
