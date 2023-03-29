for i in $(cat Sample.list)
do
cd  $i
python3 DifferentMethodSV2pbsv_DominntVCF.py -m ${i}.merged.vcf -s $i -o ${i}.integrated.vcf
cd ..
done
