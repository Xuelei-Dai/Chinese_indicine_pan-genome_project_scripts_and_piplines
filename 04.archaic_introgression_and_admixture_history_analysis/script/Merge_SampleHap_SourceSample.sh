Sample_Hap1_VCF=$1
Sample_Hap2_VCF=$2
Source_Sample_VCF=$3
OUT_VCF=$4
bcftools merge ${Sample_Hap1_VCF} ${Sample_Hap2_VCF} ${Source_Sample_VCF} -O z -o ${OUT_VCF}
bcftools index ${OUT_VCF}
