for name in $(cat ../sample.txt)
do
	count=$((${count}+1))
	echo ${name}
	echo ${count}
	if [ "${count}" == "1" ]; then
		
		cat ${name}_ASE1.o |sed "1i chr\tpos\t${name}_ref\t${name}_alt\t${name}_other" > ./ASE1_o_middle/${name}_${count}_o_middle
	else
		cat ${name}_ASE1.o | awk '{print $3 "\t" $4 "\t" $5}' |sed "1i ${name}_ref\t${name}_alt\t${name}_other" > ./ASE1_o_middle/${name}_${count}_o_middle

	fi
done
