args<-commandArgs(TRUE)
inFile=args[1]
outFile=args[2]
mydata=read.table(inFile,head=T,sep="\t")
print(dim(mydata))
class <- table(as.character(mydata[,2]))
lbls=paste(names(class),class,sep="\n")
print(lbls)
pdf(outFile)
par(mar=c(4,4,4,4))
pie(class,labels=lbls,cex=1.1)
dev.off()
