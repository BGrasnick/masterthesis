library(genefilter)
library(tictoc)

args = commandArgs(trailingOnly=TRUE)

rawData <- read.csv(args[1])

tic("total")

geneExpressionMatrix <- rawData[-c(1,2)]

rV <- rowVars(t(geneExpressionMatrix))

ordered <- rV[order(-rV) , drop = FALSE]

orderedNameList <- gsub("\\.", "|", names(ordered))

orderedNameValueList <- c(orderedNameList,data.frame(ordered)[,1],order(rV, decreasing=TRUE))

orderedNameValueMatrix <- matrix(orderedNameValueList,ncol=3)

colnames(orderedNameValueMatrix) <- c("attributeName", "value", "index")

toc()

write.csv(orderedNameValueMatrix, file = args[2], row.names = FALSE)