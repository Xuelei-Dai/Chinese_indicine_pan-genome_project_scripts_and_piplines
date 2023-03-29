# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 16:05:53 2023
@Mail: daixuelei2014@163.com
@author:daixuelei
"""

import logging,os,sys
import click,re


logging.basicConfig(filename=os.path.basename(__file__).replace('.py','.log'),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")


def Load_SV_INFO_Dict(File):
    Dict = {}
    for line in File:
        line = line.strip()
        if line.startswith('#'):
            pass
        else:
            line = line.split('\t')
            End = re.findall(r'END=\w*',line[7])[0].split('=')[1]
            Pos_INFO = line[0] + '_' + line[1] + '_' + End
            Dict[line[2]] = Pos_INFO
    return Dict

@click.command()
@click.option('-v','--vcf',type=click.File('r'),help='input the SV VCF file',required=True)
@click.option('-s','--svid',type=click.File('r'),help='input the SV id list file,such as:dabieshan_Hap1|DEL.409',required=True)
@click.option('-o','--out',type=click.File('w'),help='output the SV ID bed file',required=True)
def main(vcf,svid,out):
    SV_INFO_Dict = Load_SV_INFO_Dict(vcf)
    for line in svid:
        line = line.strip().split('|')
        PosINFO = SV_INFO_Dict[line[1]]
        PosINFO = PosINFO.replace('_','\t')
        out.write(f'{PosINFO}\t{line[1]}\t{line[0]}\n')

if __name__ == '__main__':
    main()
        

