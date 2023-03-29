#!/bin/bash

set -e

WORKDIR=$1
N_PERMUTATIONS=$2
POP1=$3
POP2=$4
VCF_FILE=$5

filename=`basename $VCF_FILE`
base=`basename $filename .vcf`

PERM_DIR=$WORKDIR/permutations
FST_DIR=$WORKDIR/fst
PVALUE_DIR=$WORKDIR/pvalues

mkdir -p $PERM_DIR
mkdir -p $FST_DIR
mkdir -p $PVALUE_DIR

PERM_FL=$PERM_DIR/$filename.gz
FST_FL=$FST_DIR/$filename
PVALUE_FL=$PVALUE_DIR/$base.tsv

echo "Generating permutations"
python3 generate_permutations.py \
       --input-vcf $VCF_FILE \
       --output-gz-vcf $PERM_FL \
       --n-permutations $N_PERMUTATIONS

echo "Computing FST scores"
vcftools --gzvcf $PERM_FL \
         --weir-fst-pop $POP1 \
         --weir-fst-pop $POP2 \
         --out $FST_FL

echo "Computing p-values"
python3 calculate_pvalues.py \
       --permutation-fst $FST_FL.weir.fst \
       --output-fl $PVALUE_FL
       
       
