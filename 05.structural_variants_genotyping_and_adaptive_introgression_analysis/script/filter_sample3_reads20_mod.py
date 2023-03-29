# -*- coding: utf-8 -*-
"""
Created on Wed Jan 12 21:08:43 2022

@author: funong_luo
@Mail: funong_luo@163.com

"""

import logging,os,sys
import click

logging.basicConfig(filename=os.path.basename(__file__).replace('.py','.log'),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")


@click.command()
@click.option('-l','--asefile',type=click.File('r'),help='input the ase middle file',required=True)
@click.option('-o','--out',type=click.File('w'),help='output the result file',required=True)

def main(asefile,out):
    reads_d={}
    for line in asefile:
        line = line.strip().split('\t')
        if line[0] == 'chr':
            header = '\t'.join(line)
            out.write(f'{header}\n')
            
        else:
            if (len(line) - 2) % 3 == 0: 
                ind_num = int((len(line) - 2) / 3)
                
                
            else:
                print('The number of columns is wrong, please check it!')
                break
            for i in range(ind_num):
                j = i + 1
                reads_d[j] = int(line[3 * j - 1]) + int(line[3 * j]) + int(line[3 * j + 1]) 
            if len([i for i in reads_d.values() if i >= 20]) >=3:
                raw = '\t'.join(line)
                out.write(f'{raw}\n')

if __name__ == '__main__':
    main()   



