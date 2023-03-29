# -*- coding: utf-8 -*-
#!/usr/bin/env python3
'''
Created on Thu Mar 21 15:44:48 CST 2019
@Mail: minnglee@163.com
@Author: Ming Li
'''

import sys,os,logging,click

logging.basicConfig(filename=os.path.basename(__file__).replace('.py','.log'),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")

def LoadAccession(File,InDict):
    '''
    accession       accession.version       taxid   gi
    A00002  A00002.1        9913    2
    A00003  A00003.1        9913    3
    '''
    Dict = {}
    for line in File:
        line = line.strip().split()
        if line[1] in InDict: Dict[line[1]] = line[2]
    return Dict
def LoadLineages(File,TaxList):
    '''
    tax_id,superkingdom,phylum,class,order,family,genus,species,cohort,forma,infraclass,infraorder,kingdom,no rank,no rank1,no rank10,no rank11,no rank12,no rank13,no rank14,no rank15,no rank16,no rank17,no rank18,no rank19,no rank2,no rank20,no rank21,no rank3,no rank4,no rank5,no rank6,no rank7,no rank8,no rank9,parvorder,species group,species subgroup,species1,subclass,subfamily,subgenus,subkingdom,suborder,subphylum,subspecies,subtribe,superclass,superfamily,superfamily1,superorder,superphylum,tribe,varietas
    1,,,,,,,,,,,,,root,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
    2,Bacteria,,,,,,,,,,,,cellular organisms,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
    6,Bacteria,Proteobacteria,Alphaproteobacteria,Rhizobiales,Xanthobacteraceae,Azorhizobium,,,,,,,cellular organisms,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
    '''
    Dict = {}
    Index = []
    for line in File:
        line = line.strip().split(',')
        if line[0] == 'tax_id':
            for i in TaxList:
                Index.append(line.index(i))
        Info = []
        for i in Index: Info.append(line[i])
        Dict[line[0]] = '|'.join(Info)
    return Dict
@click.command()
@click.option('-i','--input',type=click.File('r'),help='The input file',required=True)
@click.option('-l','--lineages',type=str,help='The lineages csv file',required=True)
@click.option('-a','--accession',type=str,help='The nucl_gb accession 2 taxid file',required=True)
@click.option('-o','--output',type=click.File('w'),help='The output file',required=True)
def main(input,lineages,accession,output):
    '''
    ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/accession2taxid/nucl_gb.accession2taxid.gz
    ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/accession2taxid/prot.accession2taxid.gz
    https://gitlab.com/zyxue/ncbitax2lin-lineages/blob/master/lineages-2019-02-20.csv.gz
    
    Chahua_2#chahua_0#2739255#2743492       AC171016.2      80.69   4237    347     45      11      224     553     129059  128718  3e-61   250     8
    Chahua_2#chahua_0#5940096#5940636       XR_003072872.1  95.32   540     406     16      3       128     532     166     569     5e-180  641     75
    '''
    InDict = {}
    for line in input:
        line = line.strip().split()
        InDict[line[1]] = None
    input.seek(0)
    #### Load lineages
    TaxList = ['kingdom','phylum','subphylum','class','order','family','genus','species']
    Lineages = LoadLineages(os.popen(f'less {lineages}'),TaxList)
    print('Lineages loaded!')
    #### Load accession
    if accession.endswith('.gz'):
        AccessionDict = LoadAccession(os.popen(f'less {accession}'),InDict)
    else: AccessionDict = LoadAccession(open(accession),InDict)
    print('Accession loaded!')
    #### output
    for line in input:
        line = line.strip()
        AccessionID = line.split()[1]
        if AccessionID in AccessionDict: 
            if AccessionDict[AccessionID] in Lineages: output.write(f"{line}\t{Lineages[AccessionDict[AccessionID]]}\n")
            else: output.write(f"{line}\t{('NA|'*len(TaxList)).strip('|')}\n")
        else: output.write(f"{line}\t{('NA|'*len(TaxList)).strip('|')}\n")
if __name__ == '__main__':
    main()
