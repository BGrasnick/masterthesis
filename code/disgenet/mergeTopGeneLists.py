import pandas as pd
import glob

geneSet = set()

path = "../../data/disgenet/selectedTop10/*.tsv"


for fname in glob.glob(path):	
	df = pd.read_csv(fname)

	geneSet.update(df["c2.symbol"].tolist())


with open("../../data/disgenet/mergedList.csv", "w") as outputfile:
	for item in geneSet:
  		outputfile.write("%s\n" % item)