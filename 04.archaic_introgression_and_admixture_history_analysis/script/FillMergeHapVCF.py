# -*- coding: utf-8 -*-
"""
Created on Wed Nov 17 17:16:28 2021
@Mail: daixuelei2014@163.com
@author:daixuelei
"""

import logging,os,sys
import click
import gzip

logging.basicConfig(filename=os.path.basename(__file__).replace('.py','.log'),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")

@click.command()
@click.option('-v','--vcf',type=str,help='input vcf file',required=True)
@click.option('-o','--out',type=click.File('w'),help='output the fill Haplotype VCF file',required=True)
def main(vcf,out):
    f = gzip.open(vcf,'rb')
    for line in f:
        line = line.decode().strip()
        if line.startswith('##'):
            out.write(f'{line}\n')
        elif line.startswith('#'):
            line = line.split('\t')
            PreINFO = '\t'.join(line[:9])
            SampleName = line[9].split('_')[0]
            out.write(f'{PreINFO}\t{SampleName}\n')
        else:
            line = line.split('\t')
            PreINFO = '\t'.join(line[:9])
            Hap1_GT = line[9].replace('/','|').split('|')[0].replace('.','0')
            Hap2_GT = line[10].replace('/','|').split('|')[1].replace('.','0')
            GT = Hap1_GT + '|' + Hap2_GT
            out.write(f'{PreINFO}\t{GT}\n')

if __name__ == '__main__':
    main()