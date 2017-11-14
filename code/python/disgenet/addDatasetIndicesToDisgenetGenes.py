def addDatasetIndicesToDisgenetGenes(topGeneList, featureNames):

    outputList = []

    for tup in topGeneList:
        if tup[0] in featureNames:
            outputList.append((tup[0], tup[1], featureNames.index(tup[0]), tup[2]))

    return outputList
