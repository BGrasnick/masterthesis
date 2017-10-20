import operator, glob, csv

import pandas as pd
import pdb


def interleaveTopGeneLists(path, mergedTopGenesFileName, includeIndex):

    genesExisting = set()

    interleavedGeneList = []

    # loop through all files in the selected top genes location
    for fname in glob.glob(path):
        df = pd.read_csv(fname)

        geneList = [tuple(x) for x in df.to_records(index=False)]
        sortedGeneList = sorted(geneList, key=operator.itemgetter(1), reverse=True)
        interleavedGeneList.append(sortedGeneList)

    sortedInterleavedGeneList = []

    for index in range(len(interleavedGeneList[0])):

        sortedInterleavedGeneList.append([tup for tup in sorted([item[index] for item in interleavedGeneList if len(item) > index], key=operator.itemgetter(1), reverse=True)])

    filteredSortedInterleavedGeneList = []

    for list in sortedInterleavedGeneList:
        for tup in list:
            if not tup[0] in genesExisting:
                filteredSortedInterleavedGeneList.append(tup)
                genesExisting.add(tup[0])

    # save the sorted gene list with header
    with open(mergedTopGenesFileName, "w") as csvfile:
        csvWriter = csv.writer(csvfile, quotechar='"', quoting=csv.QUOTE_ALL)

        if includeIndex:

            return filteredSortedInterleavedGeneList

        else:

            csvWriter.writerow(["attributeName", "score", "diseaseId"])
            for tup in filteredSortedInterleavedGeneList:

                csvWriter.writerow([tup[0], tup[1], tup[2]])

