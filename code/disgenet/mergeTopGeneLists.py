import pandas as pd
import glob

def mergeTopGeneLists(path, mergedTopGenesLocation):

    geneSet = set()

    for fname in glob.glob(path):
        df = pd.read_csv(fname)

        geneSet.update(df["c2.symbol"].tolist())

    with open(mergedTopGenesLocation, "w") as outputfile:
        for item in geneSet:
            outputfile.write("%s\n" % item)
