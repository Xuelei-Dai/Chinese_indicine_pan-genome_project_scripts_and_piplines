SampleName=$1
source ~/anaconda3/envs/hmmix/bin/activate
hmmix train  -obs=obs.${SampleName}.txt -weights=ARS-UCD1.2_weights.bed -mutrates=mutationrate.bed -param=Initialguesses.json -out=trained.${SampleName}.phased.json -haploid
