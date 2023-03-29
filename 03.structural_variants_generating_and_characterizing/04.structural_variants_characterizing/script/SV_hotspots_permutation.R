### permutation test using regioneR
library(regioneR)
library(data.table)
library(dplyr)

### Input genome 
read.table("ARS-UCD1.2_ChangeNamegenome.fasta.fai") %>%  .[,c(1,2)]   ->  cattle.genome
cattle.genome <-  toGRanges(data.frame(paste("chr",cattle.genome$V1,sep=''),1,cattle.genome$V2) )  
#listChrTypes()
cattle.genome <- filterChromosomes(cattle.genome,organism ="bosTau",chr.type="canonical") 

### Input mask 
read.table("GCF_002263795.1_ARS-UCD1.2_rm.out.info.ChangeFormat") %>%  .[,c(1,2,3)] -> mask
mask$V1 <-  sub("^","chr",mask$V1)
mask <-  filterChromosomes(toGRanges(mask),chr.type="canonical")

### Input SV hotspots,all SVs, and coding genes bed files.
hotspot <- read.table("CHI.hotspot.bed")
hotspot <- toGRanges(hotspot[,c(1,2,3)]) 
all_sv <-  read.table("all_sv.bed")
all_sv$V1 <-  sub("^","chr",all_sv$V1)
all_sv <- toGRanges(all_sv)
coding_genes <- toGRanges (fread("GCF_002263795.1_ARS-UCD1.2_genomic_protein_coding_gene.changeformat.bed"))

### Permutation for coding genes and SV hotspots.
gt <- permTest(A=coding_genes,
         B=hotspot,
         ntimes=1000,
         randomize.function=circularRandomizeRegions,
         genome=cattle.genome,
         mask=mask,
         evaluate.function=numOverlaps)
          

pdf("SV_hotspots_iter_1k_.pdf", width = 5, height = 5)
plot(gt)
dev.off() 

### Permutation for coding genes and all SVs.
gr <- permTest(A=coding_genes,
         B=all_sv,
         ntimes=1000,
         randomize.function=circularRandomizeRegions,
         genome=cattle.genome,
         mask=mask,
         evaluate.function=numOverlaps)


pdf("All_SV_iter_1k.pdf", width = 5, height = 5)
plot(gr)
dev.off()
