#!/bin/bash

set -e

INPUT_VCF=$1
WORKDIR=$2
POP1=$3
POP2=$4
N_PERMUTATIONS=$5
CHUNK_SIZE=$6
N_PROC=$7

CHUNK_DIR=$WORKDIR/chunks
PVALUE_DIR=$WORKDIR/pvalues

mkdir -p $CHUNK_DIR

python3 split_vcf_file.py \
       --input-vcf $INPUT_VCF \
       --chunk-size $CHUNK_SIZE \
       --output-base $CHUNK_DIR/chunk_

find $CHUNK_DIR -name \*.vcf | parallel -j $N_PROC bash ./process_vcf.sh $WORKDIR $N_PERMUTATIONS $POP1 $POP2

cat $PVALUE_DIR/*.tsv > $WORKDIR/pvalues.tsv

python3 sort_values.py \
       --input $WORKDIR/pvalues.tsv \
       --output $WORKDIR/pvalues.sorted.tsv
