for i in $(cat Sample.list)
do
cd  $i
python3 Get_cuteSV_Uniq_SV_VCF.py -m ${i}.TotalSV.merged.vcf -s $i -o ${i}.cuteSV_uniq.vcf
cd ..
done
