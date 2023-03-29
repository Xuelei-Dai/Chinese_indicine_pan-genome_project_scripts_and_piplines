SampleName=$1
source ~/anaconda3/envs/hmmix/bin/activate
hmmix decode -obs=obs.${SampleName}.txt -weights=ARS-UCD1.2_weights.bed -mutrates=mutationrate.bed -param=trained.${SampleName}.phased.json -haploid > ${SampleName}.Decode.txt
