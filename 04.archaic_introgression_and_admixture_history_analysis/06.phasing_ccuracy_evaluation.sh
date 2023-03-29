#We divided the whole genome with a sliding window of 100 kb and calculated the relative SER value of each window by using the common heterozygous phasing SNP of the long read and short read of the leiqiong cattle individual
python3 ./script/SlideWindowStatPhasingSwitchErrorRate.py -v Chinese_indicine_TGS_NGS.phase.vcf.gz -t leiqiong -n leiqiong_NGS -l ARS-UCD1.2_ChangeNamegenome.Chromosome.fasta.size -w 100000 -o TGS_NGS_leiqiong_phasing_100kb.SlideWindow.SER

#the average SER of long read relative to short read
less TGS_NGS_leiqiong_phasing_100kb.SlideWindow.SER |grep -v 'POS' |grep -v 'NA' |awk '{sum+=$2}END{print sum/NR}'

#the wig file of common heterozygous phasing SNP was randomly selected in 100 previous divided windows
python3 ./script/SlideWindowSplitGenome2RandBed.py -l ARS-UCD1.2_ChangeNamegenome.Chromosome.fasta.size -w 100000 -n 100  -s 12345 -o ARS-UCD1.2_100Rand100kbSlideWindow.bed

less ARS-UCD1.2_100Rand100kbSlideWindow.bed | awk '{print $1":"$2"-"$3}' > ARS-UCD1.2_100Rand100kbSlideWindow.Region

mkdir -p HeterozygoteSiteHapWigFile
cd HeterozygoteSiteHapWigFile
python3 ../script/GetHeterozygoteSiteHapWigFromPhasedVCF.py -v ../Chinese_indicine_TGS_NGS.phase.vcf.gz -t leiqiong -n leiqiong_NGS -r ../ARS-UCD1.2_100Rand100kbSlideWindow.Region
