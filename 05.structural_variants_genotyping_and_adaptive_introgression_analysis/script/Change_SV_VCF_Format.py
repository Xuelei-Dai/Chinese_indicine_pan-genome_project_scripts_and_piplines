# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 16:45:49 2023
@Mail: daixuelei2014@163.com
@author:daixuelei
"""

import logging,os,sys
import click,re


logging.basicConfig(filename=os.path.basename(__file__).replace('.py','.log'),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")


@click.command()
@click.option('-v','--vcf',type=click.File('r'),help='input the SV VCF file',required=True)
@click.option('-o','--out',type=click.File('w'),help='output the vcf file',required=True)
def main(vcf,out):
    for line in vcf:
        line = line.strip()
        if line.startswith('##'):
            out.write(f'{line}\n')
        elif line.startswith('#CHROM'):
            line = line.split('\t')
            header = '\t'.join(line[:10])
            out.write(f'{header}\n')
        else:
            line = line.split('\t')
            Pre_INFO = '\t'.join(line[:7])
            SVTYPE = re.findall(r'SVTYPE=\w*',line[7])[0].split('=')[1]
            if SVTYPE == 'DEL':
                SVLEN = re.findall(r'SVLEN=-\w*',line[7])[0].split('-')[1]
                END = str(int(line[1]) + int(SVLEN))
                INFO = f'SVTYPE=DEL;END={END};SVLEN=-{SVLEN}'
            elif SVTYPE == 'INS':
                SVLEN = re.findall(r'SVLEN=\w*',line[7])[0].split('=')[1]
                INFO = f'SVTYPE=INS;END={line[1]};SVLEN={SVLEN}' 
            else:
                pass
            out.write(f'{Pre_INFO}\t{INFO}\tGT\t1/1\n')

if __name__ == '__main__':
    main()
            
            
        