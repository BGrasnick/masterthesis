library(genefilter)
library(tictoc)

rawData <- read.csv("../../data/GDC/TCGA-GBM_TCGA-THCA_TCGA-LAML_TCGA-HNSC_TCGA-LUAD_TCGA-UCEC_TCGA-KIRC_TCGA-SARC__GeneExpressionQuantification_TP_TB_HTSeq-Counts_WithDiseaseCodes.csv")

tic("total")

tic("rowVars FS")

geneExpressionMatrix <- rawData[-c(1,2)]

rV <- rowVars(t(geneExpressionMatrix))

toc()

ordered <- rV[order(-rV) , drop = FALSE]

orderedNameList <- gsub("\\.", "|", names(ordered))

orderedNameValueList <- c(orderedNameList,data.frame(ordered)[,1],order(rV, decreasing=TRUE))

orderedNameValueMatrix <- matrix(orderedNameValueList,ncol=3)

colnames(orderedNameValueMatrix) <- c("attributeName", "value", "index")

toc()

write.csv(orderedNameValueMatrix, file = "../../data/rankedAttributes/GDCrowVars.csv", row.names = FALSE)