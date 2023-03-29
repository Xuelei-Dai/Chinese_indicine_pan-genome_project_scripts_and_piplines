# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 22:22:06 2022
@Mail: daixuelei2014@163.com
@author:daixuelei
"""

import logging,os,sys
import click

logging.basicConfig(filename=os.path.basename(__file__).replace('.py','.log'),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")

def LoadSampleList(File):
    List = []
    for line in File:
        line = line.strip()
        List.append(line)
    return List

def LoadSampleMapDict(File):
    Dict = {}
    for line  in File:
        line = line.strip().split('\t')
        Dict[line[0]] = line[1]
    return Dict       

@click.command()
@click.option('-v','--vcf',type=str,help='input vcf.gz file',required=True)
@click.option('-s','--samplelist',type=click.File('r'),help='input need to extract sample list file',required=True)
@click.option('-r','--regionlist',type=click.File('r'),help='input need to extract region list',required=True)
@click.option('-m','--samplemap',type=click.File('r'),help='input sample map to species name list',required=True)
@click.option('-o','--out',type=str,help='input out results dir file',required=True)
def main(vcf,samplelist,regionlist,samplemap,out):
    SampleList = LoadSampleList(samplelist)
    SampleMapDict = LoadSampleMapDict(samplemap)
    output = os.getcwd()
    if not os.path.exists(f'{output}/{out}'): os.system(f'mkdir {output}/{out}')
    for region in regionlist:
        region = region.strip()    
        OUTPUT = open(f'{output}/{out}/{region}.fasta','w')
        for Sample in SampleList:
            Seq = os.popen(f"bcftools query -f '[%IUPACGT]' -s {Sample} -r {region} {vcf} | sed 's/.\/./N/g'").readlines()[0]
            Species = SampleMapDict[Sample]
            OUTPUT.write(f'>{Species}_{Sample}\n{Seq}\n')

if __name__ == '__main__':
    main()
   
