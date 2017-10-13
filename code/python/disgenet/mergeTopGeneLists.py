import pandas as pd
import glob, csv, operator
from collections import defaultdict

def mergeTopGeneLists(path, mergedTopGenesLocation, useThreshold, threshold, topK):

    geneDict = defaultdict()

    # loop through all files in the selected top genes location
    for fname in glob.glob(path):
        df = pd.read_csv(fname)

        # loop through all genes in this file
        for row in df.itertuples():

            # check if the gene already exists and if so which score is bigger and add the bigger score
            if row[3] not in geneDict.keys() or geneDict[row[3]][0] < row[4]:
                geneDict[row[3]] = (row[4], row[2])

    # sort the gene dictionary items by their score so that the gene with the biggest score is on top
    sorted_GeneList = sorted(geneDict.items(), key=operator.itemgetter(1), reverse=True)

    # save the sorted gene list with header
    with open(mergedTopGenesLocation, "w") as csvfile:
        csvWriter = csv.writer(csvfile, quotechar='"', quoting=csv.QUOTE_ALL)
        csvWriter.writerow(["attributeName", "score", "diseaseId"])
        for k, v in sorted_GeneList:
            csvWriter.writerow([str(k),str(v[0]), v[1]])
