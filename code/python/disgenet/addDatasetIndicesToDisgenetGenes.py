def addDatasetIndicesToDisgenetGenes(topGeneList, df):

    outputList = [("attributeName", "score", "index", "diseaseId")]

    for tup in topGeneList:
        if tup[0] in df.columns:
            outputList.append((tup[0], tup[1], df.columns.get_loc(tup[0]) - 1, tup[2]))

    return outputList
