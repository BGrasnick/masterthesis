library("genefilter", lib.loc="~/R/x86_64-pc-linux-gnu-library/3.4")

rawData <- read.csv("../../data/rawData.csv")

geneExpressionMatrix <- rawData[-c(1,2)]

rV <- rowVars(t(geneExpressionMatrix))

ordered <- rV[order(-rV) , drop = FALSE]

orderedNameList <- gsub("\\.", "|", names(ordered))

orderedNameValueList <- c(orderedNameList,data.frame(ordered)[,1],order(rV, decreasing=TRUE))

orderedNameValueMatrix <- matrix(orderedNameValueList,ncol=3)

colnames(orderedNameValueMatrix) <- c("attributeName", "value", "index")

write.csv(orderedNameValueMatrix, file = "../../data/rankedAttributes/rowVars.csv", row.names = FALSE)