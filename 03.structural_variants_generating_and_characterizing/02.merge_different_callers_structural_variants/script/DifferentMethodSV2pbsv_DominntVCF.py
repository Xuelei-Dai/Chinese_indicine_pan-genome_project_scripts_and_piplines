# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 21:52:58 2022
@Mail: daixuelei2014@163.com
@author:daixuelei
"""

import logging,os,sys
import click,re


logging.basicConfig(filename=os.path.basename(__file__).replace('.py','.log'),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")

def LoadVcfHeader():
    Header = \
        '##fileformat=VCFv4.2\n\
##source=IntergrationStructralVariantByMethod.py\n\
##INFO=<ID=CHR2,Number=1,Type=String,Description="Chromosome for END coordinate in case of a translocation">\n\
####INFO=<ID=SVTYPE,Number=1,Type=String,Description="Type of structural variant">\n\
####INFO=<ID=END,Number=1,Type=Integer,Description="End position of the structural variant described in this record">\n\
####INFO=<ID=SVLEN,Number=.,Type=Integer,Description="Difference in length between REF and ALT alleles">\n\
##ALT=<ID=DEL,Description="Deletion relative to the reference">\n\
##ALT=<ID=INS,Description="Insertion of novel sequence relative to the reference">\n\
##INFO=<ID=SVMETHOD,Number=1,Type=String,Description="Vector of samples supporting the SV">\n\
##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">' 
    return Header

@click.command()
@click.option('-m','--survivor',type=click.File('r'),help='input the survivor merged of pbsv,cutesv,sniffles,svim vcf file',required=True)
@click.option('-s','--sample',type=str,help='input the sample name',required=True)
@click.option('-o','--out',type=click.File('w'),help='output the intergrated SV VCF file',required=True)
def main(survivor,sample,out):
    VcfHeader = LoadVcfHeader()
    VcfHeaderLine = '#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT'
    out.write(f'{VcfHeader}\n{VcfHeaderLine}\t{sample}\n')
    for line in survivor:
        line = line.strip()
        if line.startswith('#'):
            pass
        else:
            line = line.split('\t')
            #FORMAT GT:PSV:LN:DR:ST:QV:TY:ID:RAL:AAL:CO
            SVTYPE = re.findall(r'SVTYPE=\w*',line[7])[0].split('=')[1]
            if SVTYPE == 'DEL' or SVTYPE == 'INS':
                if 'pbsv' in line[12]:
                    if ',' in line[12].split(':')[-1]:
                        Chrom,Pos,ID = line[12].split(':')[-1].split(',')[0].split('-')[0].split('_')[0],line[12].split(':')[-1].split(',')[0].split('-')[0].split('_')[1],line[12].split(':')[-4]
                        REF,ALT = line[12].split(':')[-3],line[12].split(':')[-2]
                        SV_TYPE,SVLEN,GT = line[12].split(':')[-5],line[12].split(':')[2],line[12].split(':')[0]
                        End = str(int(Pos) + int(SVLEN))
                    else:
                        Chrom,Pos,ID = line[12].split(':')[-1].split('-')[0].split('_')[0],line[12].split(':')[-1].split('-')[0].split('_')[1],line[12].split(':')[-4]
                        REF,ALT = line[12].split(':')[-3],line[12].split(':')[-2]
                        SV_TYPE,SVLEN,GT = line[12].split(':')[-5],line[12].split(':')[2],line[12].split(':')[0]
                        End = line[12].split(':')[-1].split('-')[1].split('_')[1]
                    if SV_TYPE == 'DEL':
                        out.write(f'{Chrom}\t{Pos}\t{ID}\t{REF}\t{ALT}\t.\tPASS\tSVTYPE=DEL;SVLEN=-{str(SVLEN)};END={End}\tGT\t{GT}\n')
                    else:
                        out.write(f'{Chrom}\t{Pos}\t{ID}\t{REF}\t{ALT}\t.\tPASS\tSVTYPE=INS;SVLEN={str(SVLEN)};END={Pos}\tGT\t{GT}\n')
                elif 'svim' in line[10]:
                    if ',' in line[10].split(':')[-1]:
                        Chrom,Pos,ID = line[10].split(':')[-1].split(',')[0].split('-')[0].split('_')[0],line[10].split(':')[-1].split(',')[0].split('-')[0].split('_')[1],line[10].split(':')[-4]
                        REF,ALT = line[10].split(':')[-3],line[10].split(':')[-2]
                        SV_TYPE,SVLEN,GT = line[10].split(':')[-5],line[10].split(':')[2],line[10].split(':')[0]
                        End = str(int(Pos) + int(SVLEN))
                    else:
                        Chrom,Pos,ID = line[10].split(':')[-1].split('-')[0].split('_')[0],line[10].split(':')[-1].split('-')[0].split('_')[1],line[10].split(':')[-4]
                        REF,ALT = line[10].split(':')[-3],line[10].split(':')[-2]
                        SV_TYPE,SVLEN,GT = line[10].split(':')[-5],line[10].split(':')[2],line[10].split(':')[0]
                        End = line[10].split(':')[-1].split('-')[1].split('_')[1]                       
                    if SV_TYPE == 'DEL':
                        out.write(f'{Chrom}\t{Pos}\t{ID}\t{REF}\t{ALT}\t.\tPASS\tSVTYPE=DEL;SVLEN=-{str(SVLEN)};END={End}\tGT\t{GT}\n')
                    else:
                        out.write(f'{Chrom}\t{Pos}\t{ID}\t{REF}\t{ALT}\t.\tPASS\tSVTYPE=INS;SVLEN={str(SVLEN)};END={Pos}\tGT\t0/1\n')
                elif 'sniffles' in line[9]:
                    if ',' in line[9].split(':')[-1]:
                        Chrom,Pos,ID = line[9].split(':')[-1].split(',')[0].split('-')[0].split('_')[0],line[9].split(':')[-1].split(',')[0].split('-')[0].split('_')[1],line[9].split(':')[-4]
                        REF,ALT = line[9].split(':')[-3],line[9].split(':')[-2]
                        SV_TYPE,SVLEN,GT = line[9].split(':')[-5],line[9].split(':')[2],line[9].split(':')[0]
                        End = str(int(Pos) + int(SVLEN))
                    else:
                        Chrom,Pos,ID = line[9].split(':')[-1].split('-')[0].split('_')[0],line[9].split(':')[-1].split('-')[0].split('_')[1],line[9].split(':')[-4]
                        REF,ALT = line[9].split(':')[-3],line[9].split(':')[-2]
                        SV_TYPE,SVLEN,GT = line[9].split(':')[-5],line[9].split(':')[2],line[9].split(':')[0]
                        End = line[9].split(':')[-1].split('-')[1].split('_')[1]
                    if SV_TYPE == 'DEL':
                        out.write(f'{Chrom}\t{Pos}\t{ID}\t{REF}\t{ALT}\t.\tPASS\tSVTYPE=DEL;SVLEN=-{str(SVLEN)};END={End}\tGT\t{GT}\n')
                    else:
                        out.write(f'{Chrom}\t{Pos}\t{ID}\t{REF}\t{ALT}\t.\tPASS\tSVTYPE=INS;SVLEN={str(SVLEN)};END={Pos}\tGT\t{GT}\n')

if __name__ == '__main__':
    main()

                        
                        
                        
                        
                
                
                
