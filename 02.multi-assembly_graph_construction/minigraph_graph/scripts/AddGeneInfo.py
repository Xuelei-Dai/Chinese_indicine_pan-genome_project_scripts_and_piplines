# -*- coding: utf-8 -*-
#!/usr/bin/env python3
'''
Created on Tue Apr 30 15:02:19 CST 2019
@Mail: minnglee@163.com
@Author: Ming Li
'''

import sys,os,logging,click

logging.basicConfig(filename=os.path.basename(__file__).replace('.py','.log'),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")

def LoadGeneID(File,Keep):
    '''
    #tax_id	GeneID	status	RNA_nucleotide_accession.version	RNA_nucleotide_gi	protein_accession.version	protein_gi	genomic_nucleotide_accession.versiogenomic_nucleotide_gi	start_position_on_the_genomic_accession	end_position_on_the_genomic_accession	orientation	assembly	mature_peptide_accession.version   mature_peptide_gi	Symbol
    9	1246500	-	-	-	AAD12597.1	3282737	AF041837.1	3282736	-	-	?	-	-	-	repA1
    9	1246500	PROVISIONAL	-	-	NP_047184.1	10954455	NC_001911.1	10954454	348	1190	-	-	-	-	repA1
    '''
    Dict = {}
    for line in File:
        line = line.strip().split('\t')
        if line[5] not in Keep: continue
        Dict[line[5]] = line[1]
    return Dict
def LoadGeneInfo(File,Keep):
    '''
    #tax_id	GeneID	Symbol	LocusTag	Synonyms	dbXrefs	chromosome	map_location	description	type_of_gene	Symbol_from_nomenclature_authority	Full_name_from_nomenclature_authority	Nomenclature_status	Other_designations	Modification_date	Feature_type
    7	5692769	NEWENTRY	-	-	-	-	-	Record to support submission of GeneRIFs for a gene not in Gene (Azotirhizobium caulinodans.  Use when strain, subtype, isolate, etc. is unspecified, or when different from all specified ones in Gene.).	other	-	-	-	-	20190202	-
    9	1246500	repA1	pLeuDn_01	-	-	-	-	putative replication-associated protein	protein-coding	-	-	-	-	20180129   -
    '''
    Dict = {}
    for line in File:
        line = line.strip().split('\t')
        if line[1] not in Keep: continue
        Dict[line[1]] = [line[2],line[8],line[9]]
    return Dict
@click.command()
@click.option('-i','--input',type=click.File('r'),help='The input file',required=True)
@click.option('-a','--gene2accession',type=click.File('r'),help='The gene2accession file',required=True)
@click.option('-g','--geneinfo',type=click.File('r'),help='The gene_info file',required=True)
@click.option('-o','--output',type=click.File('w'),help='The output file',required=True)
def main(input,gene2accession,geneinfo,output):
    '''
    Dweishan_2#m5-6_3263#0#2455    XP_010726389.1  96.259  2455    294     2       1       2428    1547    1       285     285     283     0.0     536     36      1.03158 Metazoa|Chordata|Craniata|Aves|Galliformes|Phasianidae|Meleagris|Meleagris gallopavo
    Daweishan_2#m5-6_2075#0#3031    OXB51536.1      88.732  3031    71      7       1       2054    2266    1       70      70      63      5.43e-29        120     7       1.01429 Metazoa|Chordata|Craniata|Aves|Galliformes|Odontophoridae|Callipepla|Callipepla squamata
    '''
    Dict = {}
    for line in input:
        line = line.strip().split()
        Dict[line[1]] = None
    #### Load GeneID
    GeneID = LoadGeneID(gene2accession,Dict)
    print('GeneID Loaded!')
    #### Load Gene Info
    GeneInfo = LoadGeneInfo(geneinfo,GeneID.values())
    print('Gene Info Loaded!')
    #### output
    input.seek(0)
    for line in input:
        Accession = line.strip().split()[1]
        if Accession in GeneID:
            if GeneID[Accession] in GeneInfo:
                Info = '\t'.join(GeneInfo[GeneID[Accession]])
                output.write(f'{line.strip()}\t{Info}\n')
            else: output.write(f'{line.strip()}\tNA\tNA\tNA\n')
        else: output.write(f'{line.strip()}\tNA\tNA\tNA\n')
if __name__ == '__main__':
    main()
