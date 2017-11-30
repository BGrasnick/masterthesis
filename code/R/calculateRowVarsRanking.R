library(genefilter)
library(tictoc)

rawData <- read.csv("../../data/GDC/TCGA-PRAD_TCGA-OV_TCGA-COAD_TCGA-LUSC_TCGA-BRCA_TCGA-PAAD_TCGA-STAD_TCGA-CESC__GeneExpressionQuantification_TP_HTSeq-Counts_WithDiseaseCodes.csv")

for (i in 1:10){
  tic("total")
  
  geneExpressionMatrix <- rawData[-c(1,2)]
  
  rV <- rowVars(t(geneExpressionMatrix))
  
  ordered <- rV[order(-rV) , drop = FALSE]
  
  orderedNameList <- gsub("\\.", "|", names(ordered))
  
  orderedNameValueList <- c(orderedNameList,data.frame(ordered)[,1],order(rV, decreasing=TRUE))
  
  orderedNameValueMatrix <- matrix(orderedNameValueList,ncol=3)
  
  colnames(orderedNameValueMatrix) <- c("attributeName", "value", "index")
  
  toc()
}

#write.csv(orderedNameValueMatrix, file = "../../data/rankedAttributes/GDCbad/rowVars.csv", row.names = FALSE)