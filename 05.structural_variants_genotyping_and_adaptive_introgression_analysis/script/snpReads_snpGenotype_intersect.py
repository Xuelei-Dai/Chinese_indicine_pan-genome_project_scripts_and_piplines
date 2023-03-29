# -*- coding: utf-8 -*-
"""
Created on Sat Jan 15 20:49:34 2022

@author: funong_luo
@Mail: funong_luo@163.com

"""

import logging,os,sys
import click

logging.basicConfig(filename=os.path.basename(__file__).replace('.py','.log'),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")

def LoadSnpgenotype(File1):
    Dict1 = {}
    for line in File1:
        line = line.strip().split()
        if line[0] == 'chr':
            Header1 = '\t'.join(line)
        else:
            TmpList = '_'.join(line[:2])    
            Dict1[TmpList] = '\t'.join(line)
    return Header1,Dict1

@click.command()
@click.option('-g','--snpgenotype',type=click.File('r'),help='input the ase middle file',required=True)
@click.option('-r','--snpreads',type=click.File('r'),help='input the ase middle file',required=True)
@click.option('-o','--out',type=click.File('w'),help='output the result file',required=True)

def main(snpgenotype,snpreads,out):
    SnpgenotypeHeader,SnpgenotypeDict = LoadSnpgenotype(snpgenotype)
    for line in snpreads:
        line = line.strip().split()
        if line[0] == 'chr':
            SnpreadsHeader = '\t'.join(line)
            out.write(f'{SnpreadsHeader}\t{SnpgenotypeHeader}\n')
        else:
            Tmplist = '_'.join(line[:2])
            snpreads_raw = '\t'.join(line)
            if Tmplist in SnpgenotypeDict.keys():
                out.write(f'{snpreads_raw}\t{SnpgenotypeDict[Tmplist]}\n')
         
if __name__=='__main__':
    main()       
