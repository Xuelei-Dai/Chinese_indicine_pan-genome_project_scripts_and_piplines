# -*- coding: utf-8 -*-
"""
Created on Mon Jan 17 15:12:05 2022

@author: funong_luo
@Mail: funong_luo@163.com

"""

import logging,os,sys
import click

logging.basicConfig(filename=os.path.basename(__file__).replace('.py','.log'),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")


@click.command()
@click.option('-i','--snpfilteredintersect',type=click.File('r'),help='input the ASE2_2_snpReads_snpGenotype_intersect_filtered.result',required=True)
@click.option('-o','--out',type=click.File('w'),help='output the changed name bed file',required=True)

def main(snpfilteredintersect,out):
    for line in snpfilteredintersect:
        line = line.strip().split()
        if line[0] == 'chr':
            pass
        else:
            for lis in line[59:63]:
                out.write(lis)
                out.write("\t")
            for n in range(len(line[63:])):
                #print(len(line[63:]))
                if float(line[63:][n]) == 0.5 and float(line[2:59][3*n])+float(line[2:59][3*n+2])+float(line[2:59][3*n+1]) >= 20:
                    if float(line[2:59][3*n])/(float(line[2:59][3*n+1])+float(line[2:59][3*n])+float(line[2:59][3*n+2]))>=0.65:
                        out.write(str(1))
                        out.write("\t")
                    elif float(line[2:59][3*n])/(float(line[2:59][3*n+1])+float(line[2:59][3*n])+float(line[2:59][3*n+2]))<=0.35:
                        out.write(str(1))
                        out.write("\t")
                    else:
                        out.write(str(0))
                        out.write("\t")
                elif float(line[63:][n]) == 0.5 and float(line[2:59][3*n])+float(line[2:59][3*n+2])+float(line[2:59][3*n+1]) < 20:
                    out.write(str(0))
                    out.write("\t")
                elif int(line[63:][n]) == 2 or 0 or 1:
                    out.write(str(0))
                    out.write("\t")
                else:
                    out.write(str(0))
                    out.write("\t")
            out.write("\n")

if __name__ == '__main__':
    main()

