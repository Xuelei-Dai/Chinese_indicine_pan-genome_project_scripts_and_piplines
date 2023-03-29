Reference=$1
SampleName=$2
Sample_Prefix=$3

source ~/anaconda3/envs/SVIM-asm/bin/activate ~/anaconda3/envs/SVIM-asm
~/anaconda3/envs/SVIM-asm/bin/svim-asm haploid ./ ~/cattle/TGS_Haplotype_Assembly_SNP_calling/${SampleName}/${Sample_Prefix}.sort.bam ${Reference} --min_sv_size 50 --max_sv_size 1000000 --sample ${Sample_Prefix}
