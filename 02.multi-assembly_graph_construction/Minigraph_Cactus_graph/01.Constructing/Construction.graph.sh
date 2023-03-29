#Make the SV graph with minigraph.
cactus-minigraph ./jobstore cattle.pg/cattle.pg.txt cattle.pg/cattle.sv.gfa.gz  --reference ARS
#Make the assembly-to-graph alignments with minigraph.
cactus-graphmap ./jobstore cattle.pg/cattle.pg.txt cattle.pg/cattle.sv.gfa.gz cattle.pg/cattle.paf  --reference ARS --outputFasta cattle.pg/cattle.sv.gfa.fa.gz
#Split the input assemblies and PAF into chromosomes using the rGFA tags in the GFA. 
cactus-graphmap-split ./jobstore ./cattle.pg/cattle.pg.txt ./cattle.pg/cattle.sv.gfa.gz ./cattle.pg/cattle.paf --outDir cattle.pg/chroms  --reference ARS
#Compute the Cactus multiple genome alignment from the assembly-to-graph minigraph mappings.
cactus-align-batch ./jobstore ./cattle.pg/chroms/chromfile.txt cattle.pg/chrom-alignments --alignOptions "--pangenome --reference ARS --outVG "
#Produce the final graph and indexes.
cactus-graphmap-join ./jobstore --vg cattle.pg/chrom-alignments/*.vg --hal cattle.pg/chrom-alignments/*.hal --outDir ./cattle.pg --outName cattle.pg --reference ARS --vcf --giraffe clip


