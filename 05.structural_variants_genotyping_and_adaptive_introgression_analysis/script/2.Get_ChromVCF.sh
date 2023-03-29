Total_VCF=$1
Structural_Variant_Type=$2
mkdir -p ../${Structural_Variant_Type}.INPUT_VCF && cd ../${Structural_Variant_Type}.INPUT_VCF
for i in {1..29} X
do
bcftools  view ${Total_VCF} -O z -o Chr${i}.vcf.gz -r $i
tabix Chr${i}.vcf.gz
done
