import os
import pandas as pd
from disgenet.utils import createOrClearDirectory


def mapToEnsemblIds(geneDiseaseAssociationsLocation, postIdMappingLocation, uniProtToEnsemblMap, featureNames, useAllUniprotIds, useAllEnsemblIds):

    createOrClearDirectory(postIdMappingLocation)

    for fname in os.listdir(geneDiseaseAssociationsLocation):

        df = pd.read_csv(os.path.join(geneDiseaseAssociationsLocation, fname), sep='\t')

        if useAllUniprotIds:

            # look if there are multiple uniprotIds per entries and replicate rows
            df_times = df["c2.uniprotId"].str.count(";") + 1

            df["df_times"] = df_times

            df = df.loc[df.index.repeat(df.df_times)].reset_index()

            # replace the duplicated uniprotIds with ascending single Ids
            lastGeneId = -1
            lastIdx = 0

            for index, elem in df.iterrows():

                if elem["df_times"] > 1:
                    if lastGeneId != elem["c2.geneId"]:
                        lastGeneId = elem["c2.geneId"]
                        lastIdx = 0

                    df.at[index,"c2.uniprotId"] = elem["c2.uniprotId"].split(";")[lastIdx].replace(".","")
                    lastIdx += 1

        indexes_to_drop = []

        # loop over the disgenet entries and convert symbol to ensemblId
        # if there are multiple ensemblIds for an entry put all in the symbol field
        # if there is no ensemblId mark entry for deletion
        for index, elem in df.iterrows():
            if elem["c2.uniprotId"].split(";")[0] in uniProtToEnsemblMap.keys():
                if len(uniProtToEnsemblMap[elem["c2.uniprotId"]]) > 1 and useAllEnsemblIds:
                    df.at[index, "c2.symbol"] = ";".join(uniProtToEnsemblMap[elem["c2.uniprotId"]])
                else:
                    df.at[index, "c2.symbol"] = uniProtToEnsemblMap[elem["c2.uniprotId"]][0]
            else:
                df.at[index,"c2.symbol"] = ""
                indexes_to_drop.append(index)

        # delete entries with no ensemblId
        indexes_to_keep = set(range(df.shape[0])) - set(indexes_to_drop)
        df = df.take(list(indexes_to_keep))

        if useAllEnsemblIds:

            # look if there are multiple ensemblIds per entries and replicate rows
            df_times = df["c2.symbol"].str.count(";") + 1

            df["df_times"] = df_times

            df = df.loc[df.index.repeat(df.df_times)].reset_index()

            lastGeneId = -1
            lastUniprotId = ""
            lastIdx = 0

            datasetIdColumn = []

            # replace the duplicated ensemblIds with ascending single Ids
            for index, elem in df.iterrows():

                if elem["df_times"] > 1:
                    if lastGeneId != elem["c2.geneId"] or lastUniprotId != elem["c2.uniprotId"]:
                        lastGeneId = elem["c2.geneId"]
                        lastUniprotId = elem["c2.uniprotId"]
                        lastIdx = 0

                    df.at[index,"c2.symbol"] = elem["c2.symbol"].split(";")[lastIdx].replace(".","")
                    lastIdx += 1

                # look if the ensemblId exists in the dataset and if so add it's id to the datasetIdColumn
                if elem["c2.symbol"] in featureNames:
                    datasetIdColumn.append(featureNames.index(elem["c2.symbol"]))
                else:
                    datasetIdColumn.append(-1)

        else:

            # replace the duplicated ensemblIds with ascending single Ids
            for index, elem in df.iterrows():

                # look if the ensemblId exists in the dataset and if so add it's id to the datasetIdColumn
                if elem["c2.symbol"] in featureNames:
                    datasetIdColumn.append(featureNames.index(elem["c2.symbol"]))
                else:
                    datasetIdColumn.append(-1)

        df.insert(0, column="datasetIdColumn", value=datasetIdColumn)

        # filter entries by the existence of their ensemblId in the dataset and only retain important columns
        df = df[df["datasetIdColumn"] != -1][["c2.symbol", "c0.score", "datasetIdColumn", "c1.diseaseId"]]

        # sort and drop duplicate ensemblIds
        df = df.sort_values('c0.score', ascending=False)

        df = df.drop_duplicates(subset="c2.symbol")

        df.to_csv(postIdMappingLocation + fname.split("/")[-1],  index=False, sep="\t")
