# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 09:19:10 2023
@Mail: daixuelei2014@163.com
@author:daixuelei
"""

import logging,os,sys
import click
import numpy as np
import pandas as pd
from pandas import Series, DataFrame

logging.basicConfig(filename=os.path.basename(__file__).replace('.py','.log'),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")


@click.command()
@click.option('-v','--vcf',type=str,help='The input include TGS and NGS SNP phased.vcf.gz file',required=True)
@click.option('-t','--tgs_sample',type=str,help='The input TGS sample name',required=True)
@click.option('-n','--ngs_sample',type=str,help='The input NGS sample name',required=True)
@click.option('-r','--regionlist',type=click.File('r'),help='input need to extract region list file,such as:chr1:1-1000 format for a line',required=True)
def main(vcf,tgs_sample,ngs_sample,regionlist):
    TGS_Hap1_GT_List,TGS_Hap2_GT_List,NGS_Hap1_GT_List,NGS_Hap2_GT_List,Chrom_List,Pos_List = [],[],[],[],[],[]
    for Region in regionlist:
        Region = Region.strip()
        VCF_INFO_List = os.popen(f'bcftools view -s {tgs_sample},{ngs_sample} -r {Region} {vcf}').readlines()
        for line in VCF_INFO_List:
            line = line.strip()
            if line.startswith('#'):
                pass
            else:
                line = line.split('\t')
                if (line[9] == '0|1' or line[9] == '1|0' ) and (line[10] == '0|1' or line[10] == '1|0'):
                    Chrom_List.append(line[0])
                    Pos_List.append(line[1])
                    TGS_Hap1,TGS_Hap2 = line[9].split('|')[0],line[9].split('|')[1]
                    NGS_Hap1,NGS_Hap2 = line[10].split('|')[0],line[10].split('|')[1]
                    TGS_Hap1_GT_List.append(TGS_Hap1),TGS_Hap2_GT_List.append(TGS_Hap2)
                    NGS_Hap1_GT_List.append(NGS_Hap1),NGS_Hap2_GT_List.append(NGS_Hap2)
        if len(TGS_Hap1_GT_List) > 0:          
            TGS_data = {'Chrom':Chrom_List,'POS':Pos_List,'Hap1':TGS_Hap1_GT_List,'Hap2':TGS_Hap2_GT_List}
            NGS_data = {'Chrom':Chrom_List,'POS':Pos_List,'Hap1':NGS_Hap1_GT_List,'Hap2':NGS_Hap2_GT_List}
            TGS_df = pd.DataFrame(TGS_data)
            NGS_df = pd.DataFrame(NGS_data)
            TGS_df.to_csv(f'{tgs_sample}_Hap1_{Region}.wig',index=False,columns=['Chrom','POS','POS','Hap1'],header=None,sep='\t')
            TGS_df.to_csv(f'{tgs_sample}_Hap2_{Region}.wig',index=False,columns=['Chrom','POS','POS','Hap2'],header=None,sep='\t')
            NGS_df.to_csv(f'{ngs_sample}_Hap1_{Region}.wig',index=False,columns=['Chrom','POS','POS','Hap1'],header=None,sep='\t')
            NGS_df.to_csv(f'{ngs_sample}_Hap2_{Region}.wig',index=False,columns=['Chrom','POS','POS','Hap2'],header=None,sep='\t')            
        TGS_Hap1_GT_List,TGS_Hap2_GT_List,NGS_Hap1_GT_List,NGS_Hap2_GT_List,Chrom_List,Pos_List = [],[],[],[],[],[]

if __name__ == '__main__':
    main()
                
            