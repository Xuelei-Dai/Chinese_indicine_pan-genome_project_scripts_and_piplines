#Convert the CCS.BAM file of the sample to a Fasta file.
#!/bin/bash
if [ $# -ne 3 ]; then
 echo "error.. need args"
 echo "command: $0 <CCS_BAM1> <CCS_BAM2> <Sample_Prefix>"
 exit 1
fi
CCS_BAM1=$1
CCS_BAM2=$2
Sample_Prefix=$3
BAM1_Prefix="`basename $1 .ccs.bam`"
BAM2_Prefix="`basename $2 .ccs.bam`"
samtools fasta -0 ${BAM1_Prefix}.hifi.fasta ${CCS_BAM1}
samtools fasta -0 ${BAM2_Prefix}.hifi.fasta ${CCS_BAM2}
cat ${BAM1_Prefix}.hifi.fasta ${BAM2_Prefix}.hifi.fasta | gzip >  ${Sample_Prefix}.hifi.fasta.gz


#De novo assembly genomes using phased assembly graphs with hifiasm(v0.15.4), which can render a primary assembly contig and two haplotype contigs (haplotype 1 and haplotype 2) for each sample.
HiFi_Fa=$1
Sample_Prefix=$2
Threads=$3
~/software/hifiasm-0.15.4/hifiasm -o ${Sample_Prefix} -t ${Threads} ${HiFi_Fa} 2> hifiasm.log


#Extract contig sequences from gfa files assembled by hifiasm software.
Sample_Prefix=$1
awk '/^S/{print ">"$2;print $3}' ${Sample_Prefix}.bp.p_ctg.gfa > ${Sample_Prefix}.bp.p_ctg.fa
awk '/^S/{print ">"$2;print $3}' ${Sample_Prefix}.bp.hap1.p_ctg.gfa > ${Sample_Prefix}.bp.hap1.p_ctg.fa
awk '/^S/{print ">"$2;print $3}' ${Sample_Prefix}.bp.hap2.p_ctg.gfa > ${Sample_Prefix}.bp.hap2.p_ctg.fa

#Statistics on contig assemblies Information
python3 ./script/StatGenome.py -i ${Sample_Prefix}.bp.p_ctg.fa -o ${Sample_Prefix}.bp.p_ctg.fa.stat
python3 ./script/StatGenome.py -i ${Sample_Prefix}.bp.hap1.p_ctg.fa -o ${Sample_Prefix}.bp.hap1.p_ctg.fa.stat
python3 ./script/StatGenome.py -i ${Sample_Prefix}.bp.hap2.p_ctg.fa -o ${Sample_Prefix}.bp.hap2.p_ctg.fa.stat

#Reference-guided scaffolding with RagTag (v2.0.1) produced the chromosome-scale assembly genome,ARS-UCD1.2 as reference genome.
Ref_fasta=$1
Contigs_fasta=$2
ragtag.py scaffold ${Ref_fasta} ${Contigs_fasta}
