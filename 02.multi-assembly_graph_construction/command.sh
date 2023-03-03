#1.Get the fasta and change name of each chromosome 
for Chr in  `cat chr`
do
    cat Assemblylist|while read a1 a2 a3
    ###dabieshan1	H1	dabieshan
    do
        seqkit grep -p "${a2}${a3}${chr}" assembly/${a1}.fa>output/${chr}/assembly/${a1}.fa
        seqkit grep -p "${chr}" assembly/ARS.fa>output/${chr}/assembly/ARS.fa
    done
done

#2.Pangenomes were constructed on a per chromosome basis using the pipeline from https://github.com/AnimalGenomicsETH/bovine-graphs
#Update the minigraph and gfatools software
#Generate pangenome graph
minigraph -xggs -t 12 assembly/ARS1.fa assembly/dabieshan1.fa assembly/dabieshan2.fa assembly/guanling1.fa assembly/guanling2.fa assembly/jinjiang1.fa assembly/jinjiang2.fa assembly/leiqiong1.fa assembly/leiqiong2.fa assembly/lincanggaofengniu1.fa assembly/lincanggaofengniu2.fa assembly/weining1.fa assembly/weining2.fa assembly/weizhou1.fa assembly/weizhou2.fa assembly/wenshangaofengniu1.fa assembly/wenshangaofengniu2.fa assembly/xiangxi1.fa assembly/xiangxi2.fa assembly/yiling1.fa assembly/yiling2.fa > graph/cattle_graph.gfa
#extract node information
awk '$1~/S/ { split($5,chr,":"); split($6,pos,":"); split($7,arr,":");print $2,length($3),chr[3],pos[3],arr[3] }' {graph.gfa} > {graph_len.tsv}
#extract edge information
awk '$1 == "L"' {graph.gfa} > {graph_link.tsv}
#Re-align each assembly to the multi-assembly graph
minigraph -t 12 --cov -x asm graph/cattle_graph.gfa assembly/${sample}.fa > remap/cattle/${sample}_cattle.gaf
#Identify bubbles in the graph
gfatools bubble {graph.gfa} > {bubble.tsv}

#3.validate the non-reference nodes and SVs in multiassembly graph
#split_hifi_fasta
seqkit split2 -s 500000 --threads 10 -O ${sample} ${sample}/${sample}.hifi.fasta.gz
#map_hifi_to_graph
GraphAligner -t 40 -g cattle_graph.gfa -f hifi_reads/${sample}/${sample}.hifi.${part}.fasta.gz -a ${sample}/${sample}.hifi.${part}.gaf -x vg
#calculate_coverage
python3 scripts/calculate_coverage_hifi.py -g cattle_graph.gfa -a aligned/${sample}/${sample}.hifi.${part}.gaf -o coverage/${sample}/${sample}.hifi.${part}
#combined_node&egde_coverage
csvtk join {${sample}.hifi.part_001_nodecov.tsv,${sample}.hifi.part_002_nodecov.tsv,${sample}.hifi.part_003_nodecov.tsv,${sample}.hifi.part_004_nodecov.tsv,${sample}.hifi.part_005_nodecov.tsv,${sample}.hifi.part_006_nodecov.tsv,${sample}.hifi.part_007_nodecov.tsv,${sample}.hifi.part_008_nodecov.tsv,${sample}.hifi.part_009_nodecov.tsv} -t -H -f1 -O --na 0| awk '{for(i=2;i<=NF;i++){a[NR]+=$i}print $1,a[NR]}' OFS="\t">${sample}.hifi.nodecov.tsv
csvtk join {${sample}.hifi.part_001_edgecov.tsv,${sample}.hifi.part_002_edgecov.tsv,${sample}.hifi.part_003_edgecov.tsv,${sample}.hifi.part_004_edgecov.tsv,${sample}.hifi.part_005_edgecov.tsv,${sample}.hifi.part_006_edgecov.tsv,${sample}.hifi.part_007_edgecov.tsv,${sample}.hifi.part_008_edgecov.tsv,${sample}.hifi.part_009_edgecov.tsv} -H -f1,2  -t -O --na 0| awk '{for(i=3;i<=NF;i++){a[NR]+=$i}print $1,$2,a[NR]}' OFS="\t">${sample}.hifi.edgecov.tsv
#calculate_bubble_support
#cattle_path_trace.tsv from pangenomes construction using the pipelie from https://github.com/AnimalGenomicsETH/bovine-graphs
#biallelic 	 10_20314 	 AltDel 	 76 	 9 	 s7,s8,s9 	 ARS,dabieshan1,guanling1,jinjiang1,jinjiang2,lincanggaofengniu1,weining1,weining2,wenshangaofengniu1,yiling1,yiling2 	 s7,s390547,s9 	 wenshangaofengniu2,xiangxi1
python3 scripts/calculate_bubble_support.py -p cattle_path_trace.tsv -e coverage/${sample}/${sample}.hifi.edgecov.tsv -o coverage/${sample}/${sample}_bubble_support.tsv

#4.identify repetitive elements
#apply RepeatMasker to classify interspersed repeats in the longest allele sequence of each variation (bubble).
RepeatMasker -pa 20 -xsmall -s -no_is -norna -nolow -cutoff 255 -frag 20000 -species "Ruminantia"  -gff -dir out  ${Segment}.fa
#apply trf to classify tandem repeats in the longest allele sequence of each variation (bubble).
trf ${Segment}.fa 2 7 7 80 10 50 2000 -d -h

#5.predicte protein-coding genes
#NR data
diamond blastx --db ${BlastDB} --query fasta/${name}.fa --out blastout/${name}.blastout -p ${Threads} --more-sensitive --max-target-seqs 1  -e 1e-10 -f 6 qseqid sseqid pident qlen length mismatch gapopen qstart qend sstart send slen nident evalue bitscore qcovhsp
cat blastout/*blastout|sed s/[a-z]*\|//g |les>Merge.RmDup.fa.blastout
python3 scripts/GetTaxonomyInfo.py -l ncbi/ncbi_lineages_2020-12-01.csv.gz -a ncbi/prot.accession2taxid.20210303 -i Merge.RmDup.fa.blastout -o Merge.RmDup.fa.blastout.tax
python3 script/AddGeneInfo.py -i Merge.RmDup.fa.blastout.tax -a ncbi/gene2accession.20210303 -g ncbi/gene_info.20210303 -o Merge.RmDup.fa.blastout.tax.gene
#other specises protein database: Bos taurus (cattle, GCF_002263795.1), Bos indicus x Bos taurus (hybrid cattle, GCA_003369695.2), Bos mutus (wild yak, GCF_000298355.1), Bison bison bison (American bison, GCF_000754665.1), Bubalus bubalis (water buffalo, GCF_000754665.1), Capra hircus (goat, GCF_001704415.1), Ovis aries (sheep, GCF_002742125.1), Mus musculus (house mouse, GCF_000001635.26), Homo sapiens (human, GCF_000001405.39)
makeblastdb -in ${speciseprotein}.faa -input_type fasta -dbtype prot -out ${BlastDB}  -parse_seqids  
diamond blastx --db ${BlastDB} --query fasta/${name}.fa --out blastout/${name}.blastout -p ${Threads} --more-sensitive --max-target-seqs 1  -e 1e-10 -f 6 qseqid sseqid pident qlen length mismatch gapopen qstart qend sstart send slen nident evalue bitscore qcovhsp
cat blastout/*blastout|sed s/[a-z]*\|//g |awk '{print $2,$0}' OFS="\t"|les>Merge.RmDup.fa.blastout
cat ${specise}.gff.gz|awk '$3=="CDS"'|cut -f1,4,5,9|sed 's/"//g'|csvtk mutate -t -f 4 -H -p "gene=(.+?);.*"|csvtk mutate -t -f 4 -H -p "Name=(.+?);.*"|csvtk mutate -t -f4 -H -p ";product=(.+?);.*" -R|sed "s/\t/#/"|sed "s/\t/#/"|awk '{print $3,$0}' OFS="\t"|csvtk join -t -H -f1 Merge.RmDup.fa.blastout - --left-join>Merge.RmDup.fa.blastout.gene
