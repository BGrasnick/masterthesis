import pandas as pd

def reduceDataset(config, datasetLocation, featureSelectionResultsLocation):

    dataset = pd.read_csv(datasetLocation)

    keggGenes = pd.read_csv(config["KEGG"]["ensemblIdListLocation"], header = None)

    disgenetRanking = pd.read_csv(featureSelectionResultsLocation + "disgenet.csv")

    if config["reduceDatasetGenesTo"] == "KEGG":
        columnList = ["diseaseCode","Unnamed: 0"]
        columnList.extend(keggGenes[0].tolist())
        reducedDataset = dataset.filter(columnList)
        reducedDataset.to_csv(config["reducedDatasetLocation"], index = False)
    elif config["reduceDatasetGenesTo"] == "disgenet":
        columnList = ["diseaseCode","Unnamed: 0"]
        columnList.extend(disgenetRanking["attributeName"].tolist())
        reducedDataset = dataset.filter(columnList)
        reducedDataset.to_csv(config["reducedDatasetLocation"], index = False)
    elif config["reduceDatasetGenesTo"] == "combine":
        combinedGenes = set(disgenetRanking["attributeName"].tolist()).union(set(keggGenes[0].tolist()))
        columnList = ["diseaseCode","Unnamed: 0"]
        columnList.extend(list(combinedGenes))
        reducedDataset = dataset.filter(columnList)
        reducedDataset.to_csv(config["reducedDatasetLocation"], index = False)

    # update the dataset feature index for each feature in the disgenet feature ranking

    for i, row in disgenetRanking.iterrows():
        disgenetRanking.set_value(i, 'index', reducedDataset.columns.get_loc(row["attributeName"]) - 1)

    disgenetRanking.to_csv(featureSelectionResultsLocation + "disgenet.csv", index=False)