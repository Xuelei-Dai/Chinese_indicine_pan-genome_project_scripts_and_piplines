# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 10:22:21 2019

@author: Gongmian
"""

from shutil import copyfile
import os
import glob
import re
import click

def list2dict(listfile):
    sample2path = {}
    
    with open(listfile, 'r') as f:
        for line in f:
            if '#' not in line:
                line0 = line.strip().split()
                sample = line0[0]
                library = line0[1]
                path = line0[2]
                
                if path[-4:] == '.sra': #sra2fastq
                    pathlist = glob.glob(re.sub('.sra$', '*.fastq.gz', path))
                    if len(pathlist) >= 1 and len(pathlist) <= 3:
                        lane = re.sub('.sra$', '', os.path.basename(path))                        
                    else:
                        print(pathlist)
                        raise Exception("Sra file error!")
                        
                else: #fastq文件单双端分lane
                    pathlist = [path]
                    if len(re.findall('_[Rr]*[12].f[a]*[s]*[t]*q.gz$', path)) == 1: #pair end
                        lane = re.sub('_[Rr]*[12].f[a]*[s]*[t]*q.gz$', '', os.path.basename(path)) + '_PE'
                    else: #single end
                        lane = re.sub('.f[a]*[s]*[t]*q.gz$', '', os.path.basename(path)) + '_SE'
                
                if sample not in sample2path:
                    sample2path[sample] = {}
                    sample2path[sample][library] = {}
                    sample2path[sample][library][lane] = []
                    sample2path[sample][library][lane].extend(pathlist)
                else:
                    if library not in sample2path[sample]:
                        sample2path[sample][library] = {}
                        sample2path[sample][library][lane] = []
                        sample2path[sample][library][lane].extend(pathlist)
                    else:
                        if lane not in sample2path[sample][library]:
                            sample2path[sample][library][lane] = []
                            sample2path[sample][library][lane].extend(pathlist)
                        else:
                            sample2path[sample][library][lane].extend(pathlist) 
                            
    return sample2path

def dict2yaml(sample2path, yamlfile):
    for sample in sample2path:
        smyaml = f'{sample}.yaml'
        copyfile(yamlfile, smyaml)
        with open(smyaml, 'a') as f:
            f.write(f'{sample}:\n  {sample}:\n')
            for library in sample2path[sample]:
                f.write(f'    {library}:\n')
                for lane, pathlist in sample2path[sample][library].items():
                    if len(pathlist) == 1: #single end
                        f.write(f'      {lane}: {pathlist[0]}\n')
                    elif len(pathlist) == 2: #pair end
                        if len(re.findall('_[Rr]*[12].fq.gz$', pathlist[0])) == 1:
                            path = re.sub('[12].fq.gz$', '{Pair}.fq.gz', pathlist[0])
                            f.write(f'      {lane}: {path}\n')
                        elif len(re.findall('_[Rr]*[12].fastq.gz$', pathlist[0])) == 1:
                            path = re.sub('[12].fastq.gz$', '{Pair}.fastq.gz', pathlist[0])
                            f.write(f'      {lane}: {path}\n')
                        else:
                            print(pathlist)
                            raise Exception("The suffix of fastq files must be in '_(R/r)[12].fq.gz' or '_(R/r)[12].fastq.gz' format")
                    elif len(pathlist) == 3: #split3 from fastqdump: pair end + single end
                        for path in pathlist:
                            if '_' not in path: #single end
                                f.write(f'      {lane}_SE: {path}\n')
                            else: #pair end
                                paths = re.sub('[12].fastq.gz$', '{Pair}.fastq.gz', path)
                                f.write(f'      {lane}_PE: {paths}\n')
                                break
                    else:
                        print(pathlist)
                        raise Exception("File number of {lane} error!")

                        
    
@click.command()
@click.option('--listfile',help='List file contains three columns: sample ID, library name, file path')
@click.option('--yamlfile',help='Template yaml file, here we use makefile.yaml')
def main(listfile, yamlfile):
    '''
    Generate the yaml file of each individual for paleomix. Information of sample, library and input file will be added to the end of the yaml file.
    Note:
    1) pair end fastq file format:
      XXX_1.fastq.gz XXX_2.fastq.gz
      XXX_1.fq.gz XXX_2.fq.gz
      XXX_R1.fastq.gz XXX_R2.fastq.gz
      XXX_R1.fq.gz XXX_R2.fq.gz
      XXX_r1.fastq.gz XXX_r2.fastq.gz
      XXX_r1.fq.gz XXX_r2.fq.gz
    2) single end fastq file format:
      XXX.fastq.gz XXX.fq.gz
    '''
    sample2path = list2dict(listfile)
    dict2yaml(sample2path, yamlfile)
    
    
if __name__ == '__main__':
    main()
    
    
