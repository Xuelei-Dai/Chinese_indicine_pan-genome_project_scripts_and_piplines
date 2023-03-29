Reference=$1
VCF=$2
SampleManifest=$3
Threads=$4
SampleName=`basename ${SampleManifest} .txt`
source ~/anaconda3/envs/paragraph/bin/activate ~/anaconda3/envs/paragraph
~/anaconda3/envs/paragraph/bin/python3 ~/anaconda3/envs/paragraph/bin/multigrmpy.py \
	--threads ${Threads} \
	-i ${VCF} \
	-m ${SampleManifest} \
	-r ${Reference} \
	-o ${SampleName}
