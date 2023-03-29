#Get VCF list and merge SV
sh ./script/get_VcfList.sh
sh ./script/merge_VCF.sh

#Change VCF format
python3 ./script/Change_Survivor_Merge_VcfGtFormat.py -v Total_sample.merged.vcf -o Total_sample.merged.ChangeFormat.vcf
python3 ./script/SurvivorVCF2ParagraphFormatVCF.py -m Total_sample.merged.vcf -r ARS-UCD1.2_ChangeNamegenome.Chromosome.fasta -s TGS -o Total_sample.merged.FinalIntegrated.vcf
python3 ./script/RemoveVcfFlankingSV.py -v Total_sample.merged.FinalIntegrated.vcf -s ARS-UCD1.2_ChangeNamegenome.Chromosome.fasta.size -l 200 -o Total_sample.merged.FinalIntegrated.filter.vcf

#Sort VCF
python3 ./script/VCF2Sort.py -v Total_sample.merged.FinalIntegrated.filter.vcf -o Total_sample.merged.FinalIntegrated.filter.sort.vcf
