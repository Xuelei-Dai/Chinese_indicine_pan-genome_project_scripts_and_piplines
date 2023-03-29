#!/bin/bash 
# Prepare the list file to generate yaml file, for example:
echo -e "sample1\tlibrary1\tsample1_library1_lane1_1.fastq.gz
	 sample1\tlibrary1\tsample1_library1_lane1_2.fastq.gz" > list

# Generate yaml file of each cattle for paleomix
# Please review the makefile.yaml for some necessary modification (i.e. change the reference or other important options). See https://paleomix.readthedocs.io/en/stable/bam_pipeline/usage.html for details.
python ./script/produce_yaml_for_paleomix.py --listfile list --yamlfile ./script/makefile.yaml

# Run paleomix
for sample in `cut -f1 list | sort -u` ; do paleomix bam_pipeline run ${sample}.yaml ; done

# Delete unused files (release storage space) after we get the final realigned BAM files
for sample in `cut -f1 list | sort -u` ; do rm $sample/reads/*/*/*/*.gz $sample/*/*/*/*/*.sai $sample/*/*/*/*/*.bam $sample/*/*/*.bam

#!/bin/bash
REF="~/Bovine_genome" # Set up the directories for softwares and bovine reference genomes(ARS_UCD1.2).
# Generate pseudo-haploid calls from bam files
ls *.nuclear.realigned.bam > all.bamlist
for chr in {1..29} X # Split the cattle genome into chromosomes
do
	angsd \
		-b all.bamlist \
		-nThreads 2 \
		-minQ 20 -minMapQ 20 -remove_bads 1 -uniqueOnly 1 \
		-C 50 -ref $REF \
		-only_proper_pairs 0 \
		-minInd 1 \
		-doCounts 1 -dumpCounts 4 \
		-dohaplocall 1 \
		-r $chr \
		-out chr${chr}
	haploToPlink chr${chr}.haplo.gz chr${chr}
	sed -i 's/N N/0 0/g' chr${chr}.tped
done

for chr in {1..29} ; do cat chr${chr}.tped ; done > chrAuto.tped

rm chr{1..29}.*.gz chrX.*.gz chr{1..29}.tped
