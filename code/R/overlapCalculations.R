library("VennDiagram", lib.loc="~/R/x86_64-pc-linux-gnu-library/3.4")
InfoGain <- read.csv("~/development/masterthesis/for_real/git_repo/data/rankedAttributes/InfoGain.csv")
GainRatio <- read.csv("~/development/masterthesis/for_real/git_repo/data/rankedAttributes/GainRatio.csv")
ReliefF <- read.csv("~/development/masterthesis/for_real/git_repo/data/rankedAttributes/ReliefF.csv")
SVM.RFE <- read.csv("~/development/masterthesis/for_real/git_repo/data/rankedAttributes/SVM-RFE.csv")
rowVars <- read.csv("~/development/masterthesis/for_real/git_repo/data/rankedAttributes/rowVars.csv")
disgenetTop25new <- read.csv("~/development/masterthesis/for_real/git_repo/data/rankedAttributes/disgenetTop25.csv")
disgenetTop25_old <- read.csv("~/development/masterthesis/for_real/git_repo/data/rankedAttributes/disgenetTop25_old.csv")

topK <- 200

overlap <- calculate.overlap(list(head(disgenetTop25new$attributeName,topK), head(disgenetTop25_old$attributeName,topK), head(rowVars$attributeName,topK)))

print(overlap$a6)

venn.diagram(list(disgenetTop25new = head(disgenetTop25new$attributeName,topK), disgenetTop25_old = head(disgenetTop25_old$attributeName,topK), RowVars = head(rowVars$attributeName,topK)), filename = "~/development/masterthesis/for_real/results/FSoverlap.tiff")


data <- c("geneName", "disgenetTop25new", "disgenetTop25_old", "rowVars")

for (geneName in overlap$a31) {
  data <- c(data, c(geneName, match(geneName , disgenetTop25new$attributeName), match(geneName , disgenetTop25_old$attributeName), match(geneName , rowVars$attributeName)))
}

matrix <- matrix(data,nrow=4)

t(matrix)

overlap2 <- calculate.overlap(list(overlap$a6, head(disgenetTop25new$attributeName,100)))
venn.diagram(list(FS = overlap$a6, DisGenet = head(disgenetTop25new$attributeName,100)), filename = "~/development/masterthesis/for_real/results/FSDisgenetoverlap.tiff")

overlap3 <- calculate.overlap(list(overlap$a6, head(disgenetTop25_old$attributeName,100)))
venn.diagram(list(FS = overlap$a6, DisGenet = head(disgenetTop25_old$attributeName,100)), filename = "~/development/masterthesis/for_real/results/FSDisgenetOldoverlap.tiff")