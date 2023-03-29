# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 16:36:29 2023
@Mail: daixuelei2014@163.com
@author:daixuelei
"""
import logging,os,sys
import click


logging.basicConfig(filename=os.path.basename(__file__).replace('.py','.log'),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")


@click.command()
@click.option('-v','--vcf',type=click.File('r'),help='input the variants.vcf of the ouput of SVIM_ASM file',required=True)
@click.option('-o','--out',type=click.File('w'),help='output the vcf file',required=True)
def main(vcf,out):
    for line in vcf:
        line = line.strip()
        if line.startswith('#'):
            out.write(f'{line}\n')
        else:
            line = line.split('\t')
            if 'DEL' in line[2] or 'INS' in line[2]:
                INFO = '\t'.join(line)
                out.write(f'{INFO}\n')
                
if __name__ == '__main__':
    main()