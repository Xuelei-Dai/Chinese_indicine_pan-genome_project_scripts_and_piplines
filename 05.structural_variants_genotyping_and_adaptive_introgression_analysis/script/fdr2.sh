for filename in ./*forFDR.txt
do
	name=$(echo "${filename##*/}" | sed 's/_ref_alt_forFDR.txt//g')
export i=${filename}
####generate a R script
echo "#!/usr/bin/env Rscript
a<-read.table(\"${i}\",header=F)
Pvalue <-array()
log2_FC<-array()
for(i in 1:nrow(a)){
if(a[i,3]==0&& a[i,4]==0){
Pvalue[i]<-\"NA\"
log2_FC[i]<-\"NA\"
}else{
y=chisq.test(matrix(c(a[i,3],a[i,4])))
Pvalue[i]<-y\$p.value
log2_FC[i]<-log2((a[i,3]+0.001)/(a[i,4]+0.001))
}}
fdr=p.adjust(Pvalue,\"BH\")
out<-cbind(a,log2_FC,Pvalue,fdr) 
write.table(out,file=\"${name}.fdr\",quote=FALSE,sep=\"\t\",row.names=FALSE)
" > ${name}.r
/stor9000/apps/users/NWSUAF/2014010669/anaconda3/envs/R-4.0.3/bin/Rscript ./${name}.r
done
