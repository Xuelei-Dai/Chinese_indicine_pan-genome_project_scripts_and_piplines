Reference=$1
BAM=$2
Threads=$3
SampleName="`basename $2`"
~/anaconda3/envs/paragraph/bin/idxdepth -b ${BAM} -r ${Reference} -o ${SampleName}.depth --threads ${Threads}
