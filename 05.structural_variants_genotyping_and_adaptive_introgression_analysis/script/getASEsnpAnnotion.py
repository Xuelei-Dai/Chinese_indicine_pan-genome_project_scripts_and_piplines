# -*- coding: utf-8 -*-
"""
Created on Tue Jan 18 11:46:54 2022

@author: funong_luo
@Mail: funong_luo@163.com

"""

import logging,os,sys
import click

logging.basicConfig(filename=os.path.basename(__file__).replace('.py','.log'),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")

def Loadannotionfile(File1):
    Dict1={}
    Dict2={}
    for line in File1:
        line = line.strip().split()
        Tmplist='_'.join(line[:2])
        if line[5] == "ncRNA_exonic" or line[5] == "exonic":
            Dict2[Tmplist] = line[5]
            Dict1[Tmplist] = line[6]
        elif line[5] == "UTR5" or line[5] == "UTR3":
            Dict2[Tmplist] = line[5]
            Dict1[Tmplist] = line[6].split('(')[0]
        else:
            pass
    return Dict1,Dict2
            

@click.command()
@click.option('-i','--asesnp',type=click.File('r'),help='input the ase middle file',required=True)
@click.option('-a','--annotion',type=click.File('r'),help='input the ase middle file',required=True)
@click.option('-o','--out',type=click.File('w'),help='output the result file',required=True)


def main(asesnp,annotion,out):
    annotionDict,posDict = Loadannotionfile(annotion)
    for line in asesnp:
        line = line.strip().split()
        Tmplist = '_'.join(line[:2])
        asesnp_raw = '\t'.join(line)
        if Tmplist in annotionDict.keys():
            out.write(f'{annotionDict[Tmplist]}\t{posDict[Tmplist]}\t{asesnp_raw}\n')

if __name__=='__main__':
    main()    
            
    



