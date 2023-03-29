# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 11:26:58 2023
@Mail: daixuelei2014@163.com
@author:daixuelei
"""

import sys,os,logging,click
from itertools import groupby

logging.basicConfig(filename=os.path.basename(__file__).replace('.py','.log'),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")

def LoadSlideWindowPosList(Length,Windows):
    Pos_INFO_List = []
    for line in Length:
        line = line.strip().split()
        for i in range(0,int(line[1]),Windows):
            if (int(line[1]) // Windows) * Windows < int(line[1]):
                Start = str(i)
                End = str(i + Windows)
                TMP = line[0] + ':' + Start + '-' + End
                Pos_INFO_List.append(TMP)
            else:
                Start = str(i)
                End = line[1]
                TMP = line[0] + ':' + Start + '-' + End
                Pos_INFO_List.append(TMP)
    return Pos_INFO_List

def Load_Sample_GT_INFO_List(VCF,Sample1,Sample2,Region):
    GT_INFO_List = []
    VCF_INFO_List = os.popen(f'bcftools view -s {Sample1},{Sample2} -r {Region} {VCF}').readlines()
    for line in VCF_INFO_List:
        line = line.strip()
        if line.startswith('#'):
            pass
        else:
            line = line.split('\t')
            if (line[9] == '0|1' or line[9] == '1|0' ) and (line[10] == '0|1' or line[10] == '1|0'):
                if line[9] == line[10]:
                    GT_INFO_List.append(0)
                else:
                    GT_INFO_List.append(1)
    return GT_INFO_List

@click.command()
@click.option('-v','--vcf',type=str,help='The input include TGS and NGS SNP phased.vcf.gz file',required=True)
@click.option('-t','--tgs_sample',type=str,help='The input TGS sample name',required=True)
@click.option('-n','--ngs_sample',type=str,help='The input NGS sample name',required=True)
@click.option('-l','--length',type=click.File('r'),help='The input genome chrom length file',required=True)
@click.option('-w','--windows',type=int,help='The input slide windowns size',default=20000)
@click.option('-o','--out',type=click.File('w'),help='The output rand slide window Phasing switch error rate file',required=True)
def main(vcf,tgs_sample,ngs_sample,length,windows,out):
    SlideWindowPosList = LoadSlideWindowPosList(length,windows)
    out.write(f'POS\tSER\n')
    for Pos in SlideWindowPosList:
        Het_GT_INFO_List = Load_Sample_GT_INFO_List(vcf,tgs_sample,ngs_sample,Pos)
        Het_GT_Num = len(Het_GT_INFO_List)
        TMP_List = [list(group) for _, group in groupby(Het_GT_INFO_List)]
        if len(TMP_List) == 0:
            out.write(f'{Pos}\tNA\n')
        else:            
            SER = round((len(TMP_List) -1) / Het_GT_Num,4)
            out.write(f'{Pos}\t{str(SER)}\n')

if __name__ == '__main__':
    main()