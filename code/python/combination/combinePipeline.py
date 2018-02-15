import pandas as pd

def executeCombinePipeline(config, resultsLocation, ensemblIdListLocation):

    keggGenes = pd.read_csv(ensemblIdListLocation, header = None)

    disgenetRanking = pd.read_csv(resultsLocation + "disgenet.csv")

    if config["combineExternalKnowledge"]:
        combinedGenes = set(disgenetRanking["attributeName"].tolist()).union(set(keggGenes[0].tolist()))

    computationalMethodRankingLocations = []

    for method in config["FS-methods"]:
        if method == "VB-FS":
            computationalMethodRankingLocations.append((pd.read_csv(resultsLocation + "VB-FS.csv"), method))
        else:
            computationalMethodRankingLocations.append((pd.read_csv(resultsLocation + method + ".csv"),method))

    for method in computationalMethodRankingLocations:

        combinationWithKEGG = method[0][method[0]['attributeName'].isin(keggGenes[keggGenes.columns[0]].tolist())]
        combinationWithDisgenet = method[0][method[0]['attributeName'].isin(disgenetRanking["attributeName"].tolist())]

        combinationWithKEGG.to_csv(resultsLocation + "KEGG_" + method[1] + ".csv", index = False)
        combinationWithDisgenet.to_csv(resultsLocation + "Disgenet_" + method[1] + ".csv", index = False)

        if config["combineExternalKnowledge"]:
            combinationWithCombinedKnowledge = method[0][method[0]['attributeName'].isin(list(combinedGenes))]
            combinationWithCombinedKnowledge.to_csv(resultsLocation + "combined_" + method[1] + ".csv", index = False)