# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 10:13:18 2021
@Mail: daixuelei2014@163.com
@author:daixuelei
"""

import logging,os,sys
import click,re

logging.basicConfig(filename=os.path.basename(__file__).replace('.py','.log'),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")

def LoadVCF(File,out):
    ChromDict = {}
    for line in File:
       line = line.strip()
       if line.startswith('#'):
           out.write(f'{line}\n')
       else:
           line = line.split('\t')
           INFO = '\t'.join(line[2:])
           Pos_INFO = (int(line[1]),INFO)
           ChromDict.setdefault(line[0],[]).append(Pos_INFO)
    return ChromDict

@click.command()
@click.option('-v','--vcf',type=click.File('r'),help='input the vcf file',required=True)
@click.option('-o','--out',type=click.File('w'),help='output the changed format VCF file',required=True)
def main(vcf,out):
    VCFINFODict = LoadVCF(vcf,out)
    VCFINFODict = dict(sorted(VCFINFODict.items(),key=lambda item:(isinstance(item[0],str),item[0])))
    for Chrom,INfo in VCFINFODict.items():
        Pos_INfo_Dict = dict(INfo)
        Pos_INfo_Dict = dict(sorted(Pos_INfo_Dict.items(),key=lambda item:item[0]))
        for pos,info in Pos_INfo_Dict.items():
            END = int(re.findall(r'END=\w*',info)[0].split('=')[1])
            if END < pos:
                END_INFO = re.findall(r'END=\w*',info)[0]
                New_END_INFO = 'END=' + str(pos)
                info.replace(END_INFO,New_END_INFO)
                out.write(f'{Chrom}\t{str(END)}\t{info}\n')
            else:
                out.write(f'{Chrom}\t{pos}\t{info}\n')

if __name__ == '__main__':
    main()
        
        
        
    