for name in $(cat sample.txt)
do
	count=$((${count}+1))
	echo ${name}
	echo ${count}
	if [ "${count}" == "1" ]; then

		cat ${name}.fdr | awk '{print $1 "\t" $2 "\t" $7}'> ./${name}_${count}_fdr_middle
	else
		cat ${name}.fdr | awk '{print $7}' > ./${name}_${count}_fdr_middle

	fi
done
