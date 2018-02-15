library(genefilter)
library(tictoc)

args = commandArgs(trailingOnly=TRUE)

if (length(args)<3) {
  stop("Please supply three arguments: inputFile (gene expression data), outputLocation (feature ranking) and geneNameSeparator", call.=FALSE)
}

rawData <- read.csv(args[1])

tic("total")

geneExpressionMatrix <- rawData[-c(1,2)]

rV <- rowVars(t(geneExpressionMatrix))

ordered <- rV[order(-rV) , drop = FALSE]

orderedNameList <- gsub("\\.", args[3], names(ordered))

orderedNameValueList <- c(orderedNameList,data.frame(ordered)[,1],order(rV, decreasing=TRUE))

orderedNameValueMatrix <- matrix(orderedNameValueList,ncol=3)

colnames(orderedNameValueMatrix) <- c("attributeName", "value", "index")

toc()

write.csv(orderedNameValueMatrix, file = args[2], row.names = FALSE)