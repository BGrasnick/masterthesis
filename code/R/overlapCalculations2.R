library("VennDiagram", lib.loc="~/R/x86_64-pc-linux-gnu-library/3.4")
InfoGain <- read.csv("~/development/masterthesis/for_real/git_repo/data/rankedAttributes/InfoGain.csv")
GainRatio <- read.csv("~/development/masterthesis/for_real/git_repo/data/rankedAttributes/GainRatio.csv")
ReliefF <- read.csv("~/development/masterthesis/for_real/git_repo/data/rankedAttributes/ReliefF.csv")
SVM.RFE <- read.csv("~/development/masterthesis/for_real/git_repo/data/rankedAttributes/SVM-RFE.csv")
rowVars <- read.csv("~/development/masterthesis/for_real/git_repo/data/rankedAttributes/rowVars.csv")
disgenetTop25 <- read.csv("~/development/masterthesis/for_real/git_repo/data/rankedAttributes/disgenetTop25.csv")
disgenetTop25_old <- read.csv("~/development/masterthesis/for_real/git_repo/data/rankedAttributes/disgenetTop25_old.csv")
disgenetTop25_interleaved <- read.csv("~/development/masterthesis/for_real/git_repo/data/rankedAttributes/disgenetTop25_interleaved.csv")

topK <- 100

overlap <- calculate.overlap(list(head(disgenetTop25$attributeName,topK), head(disgenetTop25_old$attributeName,topK), head(disgenetTop25_interleaved$attributeName,topK)))

print(overlap$a5)

venn.diagram(list(disgenetTop25 = head(disgenetTop25.csv$attributeName,topK), disgenetTop25_old = head(disgenetTop25_old$attributeName,topK), disgenetTop25_interleaved = head(disgenetTop25_interleaved$attributeName,topK)), filename = "~/development/masterthesis/for_real/results/FSoverlap.tiff")


data <- c("geneName", "disgenetTop25", "disgenetTop25_old", "disgenetTop25_interleaved")

for (geneName in overlap$a5) {
  data <- c(data, c(geneName, match(geneName , disgenetTop25$attributeName), match(geneName , disgenetTop25_old$attributeName), match(geneName , disgenetTop25_interleaved$attributeName)))
}

matrix <- matrix(data,nrow=4)

t(matrix)

overlap2 <- calculate.overlap(list(overlap$a6, head(disgenetTop25new$attributeName,100)))
venn.diagram(list(FS = overlap$a6, DisGenet = head(disgenetTop25new$attributeName,100)), filename = "~/development/masterthesis/for_real/results/FSDisgenetoverlap.tiff")

overlap3 <- calculate.overlap(list(overlap$a6, head(disgenetTop25_old$attributeName,100)))
venn.diagram(list(FS = overlap$a6, DisGenet = head(disgenetTop25_old$attributeName,100)), filename = "~/development/masterthesis/for_real/results/FSDisgenetOldoverlap.tiff")