source ~/anaconda3/envs/hmmix/bin/activate
hmmix create_ingroup  -ind=individuals.json -vcf=cattle_final.Genotype.filter.phase.vcf.gz -weights=ARS-UCD1.2_weights.bed -out=obs -outgroup=outgroup.txt -ancestral=Taurine_Indicine_ancestor.fa
