# -*- coding: utf-8 -*-
"""
Created on Wed Jan 19 15:14:24 2022

@author: funong_luo
@Mail: funong_luo@163.com

"""

import logging,os,sys
import click

logging.basicConfig(filename=os.path.basename(__file__).replace('.py','.log'),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")

def Loadannotation(File1):
    Dict1={}
    for line in File1:
        line = line.strip().split()
        key = '_'.join(line[2:4])
        Dict1[key]='\t'.join(line[0:2])
    return Dict1

def Loadasegene(File2):
    Dict2={}
    for line in File2:
        line = line.strip().split()
        if line[0] == 'gene':
            Header2 = '\t'.join(line[1:])
        else:
            Dict2[line[0]]='\t'.join(line[1:])
    return Header2,Dict2

@click.command()
@click.option('-a','--asegene',type=click.File('r'),help='input the ase middle file',required=True)
@click.option('-n','--annotation',type=click.File('r'),help='input the ase middle file',required=True)
@click.option('-i','--intersectresult',type=click.File('r'),help='input the ase middle file',required=True)
@click.option('-o','--out',type=click.File('w'),help='output the result file',required=True)

def main(intersectresult,asegene,annotation,out):
    AsegeneHeader,AsegeneDict = Loadasegene(asegene)
    annotationDict = Loadannotation(annotation)
    out.write(f'#CHROM\tSTART\tEND\tID\tSVLENGTH\t{AsegeneHeader}\tchr\tstart\tend\tgene\t{AsegeneHeader}\tPOS\tANNOV\n')
    for line in intersectresult:
        line = line.strip().split()
        keyanno = '_'.join(line[:2])
        keyase = line[-1]
        genotype = '\t'.join(line)
        if keyanno in annotationDict.keys():
            if keyase in AsegeneDict.keys():
                out.write(f'{genotype}\t{AsegeneDict[keyase]}\t{annotationDict[keyanno]}\n')
                
                
if __name__=='__main__':
    main()       

                
        



