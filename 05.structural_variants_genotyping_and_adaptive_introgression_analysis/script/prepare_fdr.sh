#snpReads_snpGenotype_intersect.rmheader.result is the file after remove header of ../snpReads_snpGenotype_intersect.result
export i=snpReads_snpGenotype_intersect.rmheader.result
cat $i |awk '{print $1"\t"$2"\t"$3"\t"$4}' > 18001_ref_alt_forFDR.txt
cat $i |awk '{print $1"\t"$2"\t"$6"\t"$7}' > 18019_ref_alt_forFDR.txt
cat $i |awk '{print $1"\t"$2"\t"$9"\t"$10}' > 18021_ref_alt_forFDR.txt
cat $i |awk '{print $1"\t"$2"\t"$12"\t"$13}' > 19030230_ref_alt_forFDR.txt
cat $i |awk '{print $1"\t"$2"\t"$15"\t"$16}' > A0097_ref_alt_forFDR.txt
cat $i |awk '{print $1"\t"$2"\t"$18"\t"$19}' > B026_ref_alt_forFDR.txt
cat $i |awk '{print $1"\t"$2"\t"$21"\t"$22}' > B070_ref_alt_forFDR.txt
cat $i |awk '{print $1"\t"$2"\t"$24"\t"$25}' > B071_ref_alt_forFDR.txt
cat $i |awk '{print $1"\t"$2"\t"$27"\t"$28}' > B072_ref_alt_forFDR.txt
cat $i |awk '{print $1"\t"$2"\t"$30"\t"$31}' > B073_ref_alt_forFDR.txt
cat $i |awk '{print $1"\t"$2"\t"$33"\t"$34}' > B078_ref_alt_forFDR.txt
cat $i |awk '{print $1"\t"$2"\t"$36"\t"$37}' > B080_ref_alt_forFDR.txt
cat $i |awk '{print $1"\t"$2"\t"$39"\t"$40}' > B081_ref_alt_forFDR.txt
cat $i |awk '{print $1"\t"$2"\t"$42"\t"$43}' > 19034_ref_alt_forFDR.txt
cat $i |awk '{print $1"\t"$2"\t"$45"\t"$46}' > B079_ref_alt_forFDR.txt
cat $i |awk '{print $1"\t"$2"\t"$48"\t"$49}' > B091_ref_alt_forFDR.txt
cat $i |awk '{print $1"\t"$2"\t"$51"\t"$52}' > B103_ref_alt_forFDR.txt
cat $i |awk '{print $1"\t"$2"\t"$54"\t"$55}' > 19043_ref_alt_forFDR.txt
cat $i |awk '{print $1"\t"$2"\t"$57"\t"$58}' > 18050051_ref_alt_forFDR.txt  
