# -*- coding: utf-8 -*-
"""
Created on Mon Jan 17 21:33:27 2022

@author: funong_luo
@Mail: funong_luo@163.com

"""

import logging,os,sys
import click

logging.basicConfig(filename=os.path.basename(__file__).replace('.py','.log'),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")


@click.command()
@click.option('-a','--asesnp',type=click.File('r'),help='input the judge_ASEsnp.result',required=True)
@click.option('-f','--fdr',type=click.File('r'),help='input the fdr file',required=True)
@click.option('-o','--out',type=click.File('w'),help='output file',required=True)

def main(asesnp,fdr,out):
    for i,j in zip(asesnp,fdr):
        print(len(j.strip().split()[2:]))
        for lis in i.strip().split()[0:4]:
            out.write(lis)
            out.write("\t")
        for n in range(len(j.strip().split()[2:])):
            if str(j.strip().split()[2:][n])=='NA':
                out.write("NA")
                out.write("\t")
            elif float(j.strip().split()[2:][n])<0.05:
                out.write(str(i.strip().split()[n+4]))
                out.write("\t")
            else:
                out.write(str(0))
                out.write("\t")
        out.write("\n")
        
if __name__=='__main__':
    main()
        
        

