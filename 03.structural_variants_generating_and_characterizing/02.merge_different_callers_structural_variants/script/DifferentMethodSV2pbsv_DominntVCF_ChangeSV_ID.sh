for i in $(cat Sample.list)
do
cd  $i
python3 DifferentMethodSV2pbsv_DominntVCF_ChangeSV_ID.py -m ${i}.merged.vcf -s $i -o ${i}.integrated_ChangeSV_ID.vcf
cd ..
done
