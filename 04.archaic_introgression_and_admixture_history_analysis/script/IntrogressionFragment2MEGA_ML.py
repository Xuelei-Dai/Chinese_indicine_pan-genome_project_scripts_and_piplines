# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 22:46:06 2022
@Mail: daixuelei2014@163.com
@author:daixuelei
"""

import sys,os,logging,click

logging.basicConfig(filename=os.path.basename(__file__).replace('.py','.log'),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")


@click.command()
@click.option('-b','--bed',type=click.File('r'),help='input Introgression_Segment.Region.list file',required=True)
@click.option('-r','--root',type=str,help='input tree /path/outgroup.txt file',required=True)
@click.option('-s','--samplehap',type=str,help='input SampleHap',required=True)
@click.option('-q','--queue',type=click.Choice(['cpu6130','jynodequeue','jyqueue','mem128queue','denovoqueue']),help='The job queue',default='jynodequeue')
@click.option('-t','--threads',type=int,help='The threads number of job',default=2)
@click.option('-m','--memory',type=int,help='The memory of job (Gb)',default=10)
def main(bed,root,samplehap,queue,threads,memory):
    output = os.getcwd()
    if not os.path.exists(f'{output}/ML_result'): os.system(f'mkdir {output}/ML_result')
    if not os.path.exists(f'{output}/ML_result/{samplehap}'): os.system(f'mkdir {output}/ML_result/{samplehap}')
    if not os.path.exists(f'{output}/log'): os.system(f'mkdir {output}/log')
    if not os.path.exists(f' {output}/log/{samplehap}'): os.system(f'mkdir {output}/log/{samplehap}')
    for line in bed:
        Region = line.strip()
        os.system(f'jsub -R "rusage[res=1]span[hosts=1]" \
                 -q {queue} \
                 -n {threads} \
                 -M {memory*1000000} \
                 -o {output}/log/{samplehap}/{samplehap}_{Region}.ML_mega.o \
                 -e {output}/log/{samplehap}/{samplehap}_{Region}.ML_mega.e \
                 -J {Region} \
                 ~/software/megacc -a ~/cattle/introgression/hmmix/Phylogenetic_Tree/infer_ML_nucleotide.mao \
                     -d {output}/Merge_Introgression_Ref_Seq/{samplehap}/{Region}.fasta -g {root} -o {output}/ML_result/{samplehap}/')
  
if __name__ == '__main__':
    main()
