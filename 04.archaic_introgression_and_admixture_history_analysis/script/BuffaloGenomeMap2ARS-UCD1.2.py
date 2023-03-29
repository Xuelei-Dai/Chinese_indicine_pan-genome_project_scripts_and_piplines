# -*- coding: utf-8 -*-
"""
Created on Fri Aug 19 09:50:56 2022
@Mail: daixuelei2014@163.com
@author:daixuelei
"""

import sys,os,logging,click
import numpy as np
import pandas as pd
from pandas import Series, DataFrame

logging.basicConfig(filename=os.path.basename(__file__).replace('.py','.log'),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")

def LoadFasta(File):
    Dict = {}
    seq = ''
    for line in File:
        line = line.strip()
        if line[0] == '>':
            if len(seq) > 0:
                Dict[name] = seq
            name = line.split()[0][1:]
            seq = ''
        else: seq += line
    Dict[name] = seq
    return Dict

def LoadAncenstorSiteDict(VCF,Sample):
    Dict ={}
    INFO_List = os.popen(f"bcftools view -s {Sample} {VCF} | grep '1|1' ").readlines()
    for line in INFO_List:
        line = line.strip().split('\t')
        Dict.setdefault(line[0],{}).update({int(line[1]):line[4]})       
    return Dict

@click.command()
@click.option('-v','--vcf',type=str,help='The input include outgroup(Buffalo) *.phased.vcf.gz file',required=True)
@click.option('-g','--genome',type=click.File('r'),help='The input reference genome',required=True)
@click.option('-s','--sample',type=str,help='The input ancenstor sample name, such as: SRR12452300',required=True)
@click.option('-o','--out',type=click.File('w'),help='The output map ancenstor genome',required=True)
def main(vcf,genome,sample,out):
    FaDict = LoadFasta(genome)
    n = 1
    NewSeq = ''
    AncenstorSiteDict = LoadAncenstorSiteDict(vcf,sample)
    for Chrom,Seq in FaDict.items():
        SubAncenstorSiteDict = AncenstorSiteDict[Chrom]
        for Base in Seq:
            if n in SubAncenstorSiteDict:
                Base = SubAncenstorSiteDict[n]
            n += 1
            NewSeq += Base
        Length = len(NewSeq)
        out.write(f'>ANCESTOR_for_chromosome:ARS-UCD1.2:{Chrom}:1:{Length}:1\n{NewSeq}\n')
        n = 1
        NewSeq = ''

if __name__ == '__main__':
    main()
            
            
  
            
    
    
    
    
    
    
    
    
    
    
    
    