# -*- coding: utf-8 -*-
"""
Created on Wed Jul 13 17:57:44 2022
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
logging.info(f"The command line is:\n\t~/anaconda3/envs/ete3/bin/python {' '.join(sys.argv)}")


def LoadIntrogressedFragmentTreeDict(File):
    '''
    ./introgression/hmmix/Phylogenetic_Tree/ML_result/dabieshan_Hap1/10:103066000-103091000-32680.nwk
    ./introgression/hmmix/Phylogenetic_Tree/ML_result/dabieshan_Hap1/10:14175000-14182000-5088.nwk
    '''
    Dict = {}
    for line in File:
        line = line.strip()
        SampleHap = line.split('/')[-2]
        Dict.setdefault(SampleHap,[]).append(line)
    return Dict

@click.command()
@click.option('-t','--tree',type=click.File('r'),help='The input All_Sample_BranchLength_Tree.nwk file',required=True)
@click.option('-r','--root',type=str,help='The input tree root sample name,such as: Buffalo_SRR12452300',required=True)
@click.option('-o','--out',type=str,help='The output segments classed file name',required=True)
def main(tree,root,out):
    IntrogressedFragmentTreeDict = LoadIntrogressedFragmentTreeDict(tree)
    df = pd.DataFrame()
    List_Hap = []
    #TGS_SampleList = ['dabieshan','guanling','jinjiang','leiqiong','lincanggaofengniu','weining','weizhou','wenshangaofengniu','xiangxi','yiling']
    #Banteng_Branch_Species_Set = {'Banteng','Kouprey','Gaur','Gayal'}
    #Yak_Branch_Species_Set = {'Yak','EuropeanBison','AmericanBison'}
    
    for Sample_Hap,Tree_File_List in IntrogressedFragmentTreeDict.items():
        for Tree_File in Tree_File_List:
            IntrogressedFragmentRegion = Tree_File.strip().split('/')[-1].split('-')[0] + '-' + Tree_File.strip().split('/')[-1].split('-')[1]
            
            t = Tree(Tree_File)
            t.set_outgroup(t&root)
            reroot_nw = t.write()
            rt = PhyloTree(reroot_nw)
    
            matches_Hap = rt.search_nodes(name=Sample_Hap)
            events_Hap = matches_Hap[0].get_my_evol_events()
            for ev in events_Hap:
                List_Hap.append(ev.in_seqs)
            
            Hap_Para_List = list(List_Hap[1])
            Hap_Para_List.remove(Sample_Hap)
            Hap_Para_Species_Set = set([i.split('_')[0] for i in Hap_Para_List])
            List_Hap = []
                                 
            if len(Hap_Para_Species_Set) == 1:
                Sample_Hap_Source = list(Hap_Para_Species_Set)[0]       
            else:
                Sample_Hap_Source = 'Ambiguous'

            Sample_Hap_df_Index = IntrogressedFragmentRegion + '_' + Sample_Hap
    
            df.loc[Sample_Hap_df_Index,'Source'] = Sample_Hap_Source
            
    df.to_csv(f'{out}',index=True,sep='\t')

if __name__ == '__main__':
    main()
