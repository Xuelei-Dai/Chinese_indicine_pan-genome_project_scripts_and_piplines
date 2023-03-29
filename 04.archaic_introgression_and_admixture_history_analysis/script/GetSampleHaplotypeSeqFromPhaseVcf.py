# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 16:26:07 2021
@Mail: daixuelei2014@163.com
@author:daixuelei
"""

import logging,os,sys
import click

logging.basicConfig(filename=os.path.basename(__file__).replace('.py','.log'),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")


@click.command()
@click.option('-v','--vcf',type=str,help='input *.vcf.phase.gz file',required=True)
@click.option('-b','--bed',type=click.File('r'),help='input ghost introgression info bed: block_global_true_introgression_fragments.bed',required=True)
@click.option('-o','--out',type=str,help='input out results dir file',required=True)
def main(vcf,bed,out):
    output = os.getcwd()
    if not os.path.exists(f'{output}/{out}'): os.system(f'mkdir {output}/{out}')
    Hap1_List,Hap2_List = [],[]
    for info in bed:
        info = info.strip().split()
        #bed format:10      100111462       100668060       guanling_Hap2
        Sample,Hap = info[3].split('_')[0],int(info[3].split('_Hap')[1])
        Region = info[0] + ':' + info[1] + '-' + info[2]
        OUTPUT = open(f'{output}/{out}/{Region}.fasta','a+')
        VCF_INFO_List = os.popen(f'bcftools view -s {Sample} -r {Region} {vcf}').readlines()
        for line in VCF_INFO_List:
            line = line.strip()
            if line.startswith('#'):
                pass
            else:
                line = line.split('\t')
                Hap1,Hap2 = line[9].replace('/','|').split('|')[0],line[9].replace('/','|').split('|')[1]
                Hap1_List.append(line[3]) if Hap1 == '0' else Hap1_List.append(line[4])
                Hap2_List.append(line[3]) if Hap2 == '0' else Hap2_List.append(line[4])        
        Hap1_Seq,Hap2_Seq = ''.join(Hap1_List),''.join(Hap2_List)
        Hap1_List,Hap2_List = [],[]
        if Hap == 1:
            OUTPUT.write(f'>{Sample}_Hap1\n{Hap1_Seq}\n')
        else:
            OUTPUT.write(f'>{Sample}_Hap2\n{Hap2_Seq}\n')
        OUTPUT.close()

if __name__ == '__main__':
    main()
                
            
    
    
