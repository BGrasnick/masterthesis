import pandas as pd
import glob, csv, operator
from collections import defaultdict

def mergeTopGeneLists(path, mergedTopGenesLocation):

    geneDict = defaultdict()

    for fname in glob.glob(path):
        df = pd.read_csv(fname)

        for row in df.itertuples():

            if row[3] in geneDict.keys():
                print(row[3])
                print(row[4])

            if row[3] not in geneDict.keys() or geneDict[row[3]] < row[4]:
                geneDict[row[3]] = row[4]

    sorted_GeneList = sorted(geneDict.items(), key=operator.itemgetter(1), reverse=True)

    with open(mergedTopGenesLocation, "w") as csvfile:
        csvWriter = csv.writer(csvfile, quotechar='"', quoting=csv.QUOTE_ALL)
        csvWriter.writerow(["attributeName","score"])
        for k, v in sorted_GeneList:
            csvWriter.writerow([str(k),str(v)])
