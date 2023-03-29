# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 13:43:20 2021
@Mail: daixuelei2014@163.com
@author:daixuelei
"""

import logging,os,sys
import click,re


logging.basicConfig(filename=os.path.basename(__file__).replace('.py','.log'),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")

@click.command()
@click.option('-v','--vcf',type=click.File('r'),help='input the vcf file',required=True)
@click.option('-o','--out',type=click.File('w'),help='output the changed format vcf file',required=True)
def main(vcf,out):
    GT_List = []
    for line in vcf:
        line = line.strip()
        if line.startswith('##'):
            out.write(f'{line}\n')
        elif line.startswith('#CHROM'):
            SampleNum = len(line.split('\t')) - 9
            out.write(f'{line}\n')
        else:
            line = line.split('\t')
            Prefix_INFO = '\t'.join(line[:8]) + '\t' + 'GT'
            #由于有些变异在svim软件找到了该SV但是基因型却显示没有，为了后续判定特异加上该个体的基因型
            for i in range(SampleNum):
                if 'svim' in line[(9+i)].split(':')[-4] and line[(9+i)].split(':')[-1] != 'NAN' and line[(9+i)].split(':')[0] == './.':
                    GT = '0/1'
                    GT_List.append(GT)
                else:  
                    GT = line[(9+i)].split(':')[0]
                    GT_List.append(GT)
            GT_INFO = '\t'.join(GT_List)
            GT_List = []
            out.write(f'{Prefix_INFO}\t{GT_INFO}\n')                

if __name__ == '__main__':
    main()