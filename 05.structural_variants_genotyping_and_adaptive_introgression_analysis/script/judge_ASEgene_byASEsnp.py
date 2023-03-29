# -*- coding: utf-8 -*-
"""
Created on Tue Jan 18 17:38:39 2022

@author: funong_luo
@Mail: funong_luo@163.com

"""

import logging,os,sys
import click
import numpy as np  
import pandas as pd  
from pandas import DataFrame  
from pandas import Series 

logging.basicConfig(filename=os.path.basename(__file__).replace('.py','.log'),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")

@click.command()
@click.option('-a','--asesnpannotion',type=str,help='input the ASE3_1_getASEsnpAnnotion.result',required=True)

@click.option('-o','--out',type=str,help='output the result file',required=True)


def main(asesnpannotion,out):
    df = pd.read_csv(f'{asesnpannotion}',sep='\t',header=None,low_memory=False)
    DF = pd.DataFrame()
    Gene_list = (df.iloc[:,0].unique()).tolist()
    for Gene in Gene_list:
        Sub_df = df[df.iloc[:,0]==Gene]
        for columns in Sub_df.columns[6:]:
            Tmp_df = Sub_df[Sub_df.iloc[:,columns]==1]
            if Tmp_df.shape[0] > 1:
                DF.loc[Gene,columns] = 'T'
            else:
                DF.loc[Gene,columns] = 'F'
    DF.to_csv(f'{out}',sep='\t',index=True)
    
                 
if __name__ == '__main__':
    main()   
    

                