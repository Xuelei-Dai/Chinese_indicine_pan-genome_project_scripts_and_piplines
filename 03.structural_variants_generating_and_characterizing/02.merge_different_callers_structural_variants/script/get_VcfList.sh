#sniffles
for i in $(cat Sample.list)
do
mkdir -p  $i
echo "~/sniffles/$i/$i.changedFormat.vcf" >> $i/$i.vcf_files_raw_calls.txt
done

#SVIM
for i in $(cat Sample.list)
do
mkdir -p  $i
echo "~/SVIM/$i/variants.vcf" >> $i/$i.vcf_files_raw_calls.txt
done

#cuteSV
for i in $(cat Sample.list)
do
mkdir -p  $i
echo "~/cuteSV/$i/$i.vcf" >> $i/$i.vcf_files_raw_calls.txt
done

#pbsv
for i in $(cat Sample.list)
do
mkdir -p  $i
echo "~/pbsv/$i/$i.vcf" >> $i/$i.vcf_files_raw_calls.txt
done
