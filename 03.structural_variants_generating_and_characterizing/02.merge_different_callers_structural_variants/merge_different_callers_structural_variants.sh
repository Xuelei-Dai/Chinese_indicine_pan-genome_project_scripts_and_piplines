##Merge the SV obtained by different callers
#Get VCF list 
sh ./script/get_VcfList.sh

#Merge SV using SURVIVOR
sh ./script/merge_VCF.sh

#Get the SV set dominated by pbsv software
sh ./script/DifferentMethodSV2pbsv_DominntVCF_ChangeSV_ID.sh

#Find out the unique SV for each caller software, we merge a new set
sh merge_TotalSV_VCF.sh
sh DifferentMethodSV2pbsv_DominntVCF_ChangeSV_ID_TotalSV.sh
sh Get_cuteSV_Uniq_SV_VCF.sh
