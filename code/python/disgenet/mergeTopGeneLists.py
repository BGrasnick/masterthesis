import pandas as pd
import os, operator, pdb
from collections import defaultdict

def mergeTopGeneLists(path, useThreshold, threshold, topK):

    geneDict = defaultdict()

    # loop through all files in the selected top genes location
    for fname in os.listdir(path):

        df = pd.read_csv(os.path.join(path, fname))

        # loop through all genes in this file
        for row in df.itertuples():

            # check if the gene already exists and if so which score is bigger and add the bigger score
            if row[1] not in geneDict.keys() or geneDict[row[1]][0] < row[2]:
                geneDict[row[1]] = (row[2], row[3], row[4])

    # sort the gene dictionary items by their score so that the gene with the biggest score is on top
    sortedGeneList = sorted(geneDict.items(), key=operator.itemgetter(1), reverse=True)

    return [(key, value[0], value[1], value[2]) for key, value in sortedGeneList]


