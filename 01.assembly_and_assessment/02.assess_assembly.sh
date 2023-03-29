#Assessing assemblies completeness using BUSCO(Version 5.4.5)
FASTA=$1
OUT_Prefix=$2
source ~/anaconda3/envs/BUSCO-5.4.5/bin/activate ~/anaconda3/envs/BUSCO-5.4.5
busco -i ${FASTA} -m genome -l ~/software/busco-master/lineages/cetartiodactyla_odb10 -o ${OUT_Prefix} -c 10 -f --offline
