for i in $(cat Sample.list)
do
echo "${i}.integrated.vcf" >> vcf_files_calls.txt
done
