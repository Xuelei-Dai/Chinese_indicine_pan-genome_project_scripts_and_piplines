# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 10:32:25 2023
@Mail: daixuelei2014@163.com
@author:daixuelei
"""

import logging,os,sys
import click


logging.basicConfig(filename=os.path.basename(__file__).replace('.py','.log'),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")


@click.command()
@click.option('-v','--vcf',type=click.File('r'),help='input the merge sample hap SV and population SV *.vcf. file',required=True)
@click.option('-s','--sample_hap',type=str,help='input sample hap name',required=True)
@click.option('-o','--out',type=click.File('w'),help='output population SV ID on sample hap assembly',required=True)
def main(vcf,sample_hap,out):
    out.write(f'#{sample_hap}|SV_ID\n')
    for line in vcf:
        line = line.strip()
        if line.startswith('#'):
            pass
        else:
            line = line.split('\t')
            if 'svim_asm' not in line[2]:
                out.write(f'{line[2]}\n')
            else:
                SV_ID = line[10].split(':')[-4]
                out.write(f'{SV_ID}\n')

if __name__ == '__main__':
    main()
                
        