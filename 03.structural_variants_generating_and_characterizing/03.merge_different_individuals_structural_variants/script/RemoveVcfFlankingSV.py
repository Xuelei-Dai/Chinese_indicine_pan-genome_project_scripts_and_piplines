# -*- coding: utf-8 -*-
"""
Created on Thu Apr  1 09:54:39 2021
@Mail: daixuelei2014@163.com
@author:daixuelei
"""

##作为paragraph的输入vcf文件，对于变异在染色体的两端，小于reads的长度，是无法进行genotyping的，该脚本用于过滤该种变异的类型，防止输入文件中含有这种变异类型导致程序中断

import logging,os,sys
import click,re

logging.basicConfig(filename=os.path.basename(__file__).replace('.py','.log'),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")

def LoadChromSizeDict(File):
    Dict = {}
    for line in File:
        line = line.strip().split()
        Dict[line[0]] = int(line[1])
    return Dict

@click.command()
@click.option('-v','--vcf',type=click.File('r'),help='input the need to filter vcf file',required=True)
@click.option('-s','--size',type=click.File('r'),help='input the chrom sizes file',required=True)
@click.option('-l','--length',type=int,help='input the length od distance between two sides of chromosome',default=200)
@click.option('-o','--out',type=click.File('w'),help='output the filter vcf file',required=True)
def main(vcf,size,length,out):
    ChromSizeDict = LoadChromSizeDict(size)
    for line in vcf:
        if line.strip().startswith('#'):
            out.write(f'{line}')
        else:
            line = line.strip().split('\t')
            ChromLength = ChromSizeDict[line[0]]
            End = re.findall(r'END=\w*',line[7])[0].split('=')[1]
            if int(line[1]) > length and int(End) < (ChromLength - length):
                INFO = '\t'.join(line)
                out.write(f'{INFO}\n')

if __name__ == '__main__':
    main()
            
    
