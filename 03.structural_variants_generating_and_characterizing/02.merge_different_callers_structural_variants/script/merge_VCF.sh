for i in $(cat Sample.list)
do
cd  $i
~/software/SURVIVOR-1.0.6/Debug/SURVIVOR merge $i.vcf_files_raw_calls.txt 10 2 1 0 0 50 $i.merged.vcf
cd ..
done
