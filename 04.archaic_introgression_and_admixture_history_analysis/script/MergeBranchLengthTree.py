# -*- coding: utf-8 -*-
"""
Created on Fri Jul 15 18:02:08 2022
@Mail: daixuelei2014@163.com
@author:daixuelei
"""
import sys,os,logging,click,re
import numpy as np
import pandas as pd
from pandas import Series, DataFrame
from ete3 import Tree
from ete3 import PhyloTree

logging.basicConfig(filename=os.path.basename(__file__).replace('.py','.log'),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")


def LoadTreeDict(File):
    '''
    ./introgression/hmmix/Phylogenetic_Tree/ML_result/dabieshan_Hap1/23:41828000-41896000-23880.nwk
    ./introgression/hmmix/Phylogenetic_Tree/ML_result/dabieshan_Hap1/4:97743000-97975000-20736.nwk
    '''
    Dict = {}
    for line in File:
        line = line.strip()
        SampleHap = line.split('/')[-2]
        Region = line.split('/')[-1].split('-')[0] + '-' + line.split('/')[-1].split('-')[1]
        RegionSampleHap = Region + '_' + SampleHap
        Dict[RegionSampleHap] = line
    return Dict

@click.command()
@click.option('-t','--tree',type=click.File('r'),help='The input All_Sample_BranchLength_Tree.nwk file',required=True)
@click.option('-o','--out',type=click.File('w'),help='The output Merge_BranchLength_Tree.nwk file',required=True)
def main(tree,out):
    TreeDict = LoadTreeDict(tree) 
    for RegionSampleHap,TreeFile in TreeDict.items():
        t = Tree(TreeFile)
        Tree_Content = t.write()
        out.write(f'{RegionSampleHap}\t{Tree_Content}\n')

if __name__ == '__main__':
    main()
            
            
            
            
            
