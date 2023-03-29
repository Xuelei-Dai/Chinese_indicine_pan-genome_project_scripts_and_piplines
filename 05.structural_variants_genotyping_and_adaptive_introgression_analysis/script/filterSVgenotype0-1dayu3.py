# -*- coding: utf-8 -*-
"""
Created on Wed Aug 10 19:37:17 2022

@author: funong_luo
@Mail: funong_luo@163.com

"""

import logging,os,sys
import click

logging.basicConfig(filename=os.path.basename(__file__).replace('.py','.log'),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")


@click.command()
@click.option('-a','--asegenesvgenotype',type=click.File('r'),help='input the ase middle file',required=True)
@click.option('-o','--out',type=click.File('w'),help='output the result file',required=True)

def main(asegenesvgenotype,out):
    for line in asegenesvgenotype:
        line = line.strip().split()
        sv_info = '\t'.join(line[:5])
        genotype_info = '\t'.join(line[5:24])
        ase_info = '\t'.join(line[24:])
        if line[0] == "#CHROM":
            
            out.write(f'{sv_info}\t{genotype_info}\t{ase_info}\n')
        else:
            count = 0
            for n in range(len(line[5:24])):
                if line[5:24][n] == "0/1":
                    count = count + 1
                else:
                    pass
                if count > 2:
                    out.write(f'{sv_info}\t{genotype_info}\t{ase_info}\n')
                    break
                else:
                    pass
                
if __name__ == '__main__':
    main()
    
