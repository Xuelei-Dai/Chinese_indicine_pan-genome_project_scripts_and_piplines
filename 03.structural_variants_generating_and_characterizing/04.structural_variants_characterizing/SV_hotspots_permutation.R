###### permutation test using regioneR
library(regioneR)
library(data.table)
library(dplyr)
library(stringr)

###### Input genome 
read.table("ARS-UCD1.2_ChangeNamegenome.fasta.fai") %>%  .[,c(1,2)]   ->  cattle.genome
cattle.genome <-  toGRanges(data.frame(paste("chr",cattle.genome$V1,sep=''),1,cattle.genome$V2) )  
#listChrTypes()
cattle.genome <- filterChromosomes(cattle.genome,organism ="bosTau",chr.type="canonical") 

###### Input mask 
# repeat file
# repeat file can be downloaded via https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/002/263/795/GCF_002263795.1_ARS-UCD1.2/GCF_002263795.1_ARS-UCD1.2_rm.out.gz
fread("GCF_002263795.1_ARS-UCD1.2_rm.out.info.ChangeFormat") %>% .[which(.$`RepeatClass/Family`=="Satellite/centr")] %>% .[,c(1,2,3)] -> Satellite_mask
colnames(Satellite_mask) <-c("chr","start","end")
# gap file
fread("GCF_002263795.1_ARS-UCD1.2_genomic_gaps.txt") %>% .[which(.$accession.version %like% "^NC" )] -> gap_mask
scaffold_chrom_list <- fread("MoleculeName_RefSeqSequence_Cattle.list")  
colnames(scaffold_chrom_list) <- c('chromosome','scaffold')
# replace the scaffold name to chromosome name
replacement_dict <- setNames(scaffold_chrom_list$chromosome, scaffold_chrom_list$scaffold)
for (i in 1:nrow(gap_mask)) {
  chromosome <- gap_mask$accession.version[i]
  gap_mask$accession.version[i] <- str_replace(chromosome, "^NC.*", replacement_dict[chromosome])
}
gap_mask <- gap_mask[,c(1,2,3)]
colnames(gap_mask) <-c("chr","start","end")
# merge satellite and gap region
merge_mask <- rbind(gap_mask,Satellite_mask)
#filter out chromosome intervals
merge_mask <- merge_mask[grepl("^[0-9X]", merge_mask$chr), ]
# sort the merge mask
chromosome_order <- c(1:29, "X")
merge_mask$chr <- factor(merge_mask$chr, levels = chromosome_order, ordered = TRUE)
sorted_merge_mask <- merge_mask %>% arrange(merge_mask$chr,merge_mask$start )
# using bedtools to merge the final mask 
merge_mask_file <- "merge_mask.bed"
write.table(sorted_merge_mask, merge_mask_file, row.names = FALSE, col.names = FALSE, quote = FALSE,sep='\t')
bedtools_command <- paste0("~/anaconda3/bin/bedtools merge -i ", merge_mask_file, " > ", "bedtools_merge_mask.bed")
system(bedtools_command)
# change the mask to GRanges format
final_mask <- fread("bedtools_merge_mask.bed")
colnames(final_mask) <- c("chr","start","end")
final_mask$chr <-  sub("^","chr",final_mask$chr )
final_mask_GRanges  <-  filterChromosomes(toGRanges(final_mask),chr.type="canonical")




###### Input SV hotspots, all SVs, and coding genes bed files.
hotspot <- fread("CHI.hotspot.bed")
hotspot <- toGRanges(hotspot[,c(1,2,3)]) 
all_sv <-  read.table("all_sv.bed")
all_sv$V1 <-  sub("^","chr",all_sv$V1)
all_sv <- toGRanges(all_sv)
coding_genes <- toGRanges (fread("GCF_002263795.1_ARS-UCD1.2_genomic_protein_coding_gene.changeformat.bed"))

######  Permutation for coding genes and SV hotspots.
gt <- permTest(A=coding_genes,
               B=hotspot,
               ntimes=1000,
               randomize.function=circularRandomizeRegions,
               genome=cattle.genome,
               mask=final_mask_GRanges,
               evaluate.function=numOverlaps)


pdf("SV_hotspots_iter_1k_.pdf", width = 5, height = 5)
plot(gt)
dev.off() 

######  Permutation for coding genes and all SVs.
gr <- permTest(A=coding_genes,
               B=all_sv,
               ntimes=1000,
               randomize.function=circularRandomizeRegions,
               genome=cattle.genome,
               mask=final_mask_GRanges,
               evaluate.function=numOverlaps)


pdf("All_SV_iter_1k.pdf", width = 5, height = 5)
plot(gr)
dev.off()