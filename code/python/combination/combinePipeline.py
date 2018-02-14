import pandas as pd

def executeCombinePipeline(config):

    keggGenes = pd.read_csv(config["combination"]["KEGG"]["ensemblIdListLocation"], header = None)

    disgenetRanking = pd.read_csv(config["disgenet"]["dataLocations"]["featureRankingOutputLocation"])

    computationalMethodRankingLocations = []

    for method in config["combination"]["FS-methods"]:
        if method == "VB-FS":
            computationalMethodRankingLocations.append((pd.read_csv(config["VB-FS"]["featureRankingOutputLocation"]), method))
        else:
            computationalMethodRankingLocations.append((pd.read_csv(config["WEKA-FS"]["featureRankingOutputLocation"] + method + ".csv"),method))

    for method in computationalMethodRankingLocations:

        combinationWithKEGG = method[0][method[0]['attributeName'].isin(keggGenes[keggGenes.columns[0]].tolist())]
        combinationWithDisgenet = method[0][method[0]['attributeName'].isin(disgenetRanking["attributeName"].tolist())]

        combinationWithKEGG.to_csv(config["combination"]["resultsLocation"] + "KEGG_" + method[1] + ".csv", index = False)
        combinationWithDisgenet.to_csv(config["combination"]["resultsLocation"] + "Disgenet_" + method[1] + ".csv", index = False)