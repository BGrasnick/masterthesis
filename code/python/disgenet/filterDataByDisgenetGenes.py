import pandas as pd

def filterByDisgenetGenes(rankedGeneNameListFileName, dataLocation, outputLocation, geneNameSeparator, topK):

    rankedGeneNameList = pd.read_csv(rankedGeneNameListFileName)
    allGenes = rankedGeneNameList[rankedGeneNameList.columns[1]].head(int(topK)).tolist()
    allGenes.sort()

    df = pd.read_csv(dataLocation)

    # add column cancer_type
    allGenes.insert(0, df.columns[0])

    # filter the data so only columns with disgenet gene names remain
    filtered_df = df.filter(allGenes)

    outputFileName = outputLocation + "_" + dataLocation.split(".")[-2].split("/")[-1] + "_Top" + str(topK) + ".csv"

    filtered_df.to_csv(outputFileName, index=False)

