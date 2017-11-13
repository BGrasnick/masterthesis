import operator, glob, pdb

import pandas as pd

def interleaveGeneLists(path):

    genesExisting = set()

    listOfGeneLists = []

    # loop through all files in the selected top genes location
    for fname in glob.glob(path):
        df = pd.read_csv(fname)

        # load geneList as list of tuples
        geneList = [tuple(x) for x in df.to_records(index=False)]

        # sort geneList by score
        sortedGeneList = sorted(geneList, key=operator.itemgetter(1), reverse=True)

        # add sorted geneList to list of all geneLists
        listOfGeneLists.append(sortedGeneList)

    interleavedGeneList = []

    # calculate all the lengths of gene lists to get the all genes even from the longest list later on
    lengths = [len(geneList) for geneList in listOfGeneLists]

    for index in range(max(lengths)):

        # add index-th entry of each individual (disease-based) geneList to the interleaved list
        # and sort those index-th entries by their score
        interleavedGeneList.extend([tup for tup in sorted([item[index] for item in listOfGeneLists if len(item) > index], key=operator.itemgetter(1), reverse=True)])

    filteredSortedInterleavedGeneList = []

    # delete multiple entries, only keep the one appearing first
    for tup in interleavedGeneList:
        if not tup[0] in genesExisting:
            filteredSortedInterleavedGeneList.append(tup)
            genesExisting.add(tup[0])

    return filteredSortedInterleavedGeneList

