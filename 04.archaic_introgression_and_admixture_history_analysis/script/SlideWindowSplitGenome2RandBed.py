# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 15:13:55 2023
@Mail: daixuelei2014@163.com
@author:daixuelei
"""

import sys,os,logging,click
import random

logging.basicConfig(filename=os.path.basename(__file__).replace('.py','.log'),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")

@click.command()
@click.option('-l','--length',type=click.File('r'),help='The input genome chrom length file',required=True)
@click.option('-w','--windows',type=int,help='The input slide windowns size',default=20000)
@click.option('-n','--number',type=int,help='The input rand slide window number',default=50)
@click.option('-s','--seed',type=int,help='The input rand seed',default=12345)
@click.option('-o','--out',type=click.File('w'),help='The output rand slide window Bed file',required=True)
def main(length,windows,number,seed,out):
    Bed_INFO_List = []
    for line in length:
        line = line.strip().split()
        for i in range(0,int(line[1]),windows):
            if (int(line[1]) // windows) * windows < int(line[1]):
                Start = str(i)
                End = str(i + windows)
                TMP = line[0] + '_' + Start + '_' + End
                Bed_INFO_List.append(TMP)  
            else:
                Start = str(i)
                End = line[1]
                TMP = line[0] + '_' + Start + '_' + End
                Bed_INFO_List.append(TMP)
    random.seed(seed)
    RandSlideWindowBedList = random.sample(Bed_INFO_List,number)
    for Bed_INFO in RandSlideWindowBedList:
        Bed_INFO = Bed_INFO.replace('_','\t')
        out.write(f'{Bed_INFO}\n')

if __name__ == '__main__':
    main()
                