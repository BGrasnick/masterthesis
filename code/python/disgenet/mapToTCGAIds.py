import operator

import pandas as pd
import csv, os
from disgenet.utils import createOrClearDirectory

def mapToTCGAIds(geneDiseaseAssociationsLocation, postIdMappingLocation, featureNames, geneNameSeparator, useThreshold, threshold, topK):

    createOrClearDirectory(postIdMappingLocation)

    splitGeneNames = [geneName.split(geneNameSeparator)[0] for geneName in featureNames]

    for fname in os.listdir(geneDiseaseAssociationsLocation):

        resultList = []

        df = pd.read_csv(os.path.join(geneDiseaseAssociationsLocation, fname), sep='\t')

        if useThreshold:
            df = df[df["c0.score"] >= float(threshold)]
        else:
            if df.shape[0] >= int(topK):
                df = df.head(n=int(topK))

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

                df.at[index, "c2.uniprotId"] = elem["c2.uniprotId"].split(";")[lastIdx].replace(".", "")
                lastIdx += 1

        genesAdded = set()

        for index, elem in df.iterrows():

            # get the genes that exactly match the name (minus the separator | and the number)
            if elem["c2.symbol"]in splitGeneNames:
                matchingIndices = [splitGeneNames.index(elem["c2.symbol"])]

            # if we didn't find an exact match, look for subtypes
            else:
                matchingIndices = [splitGeneNames.index(s) for s in splitGeneNames if s.startswith(elem["c2.symbol"])]

            for matchIdx in matchingIndices:
                if not matchIdx in genesAdded:
                    resultList.append((featureNames[matchIdx], elem["c0.score"], matchIdx, elem["c1.diseaseId"]))
                    genesAdded.add(matchIdx)

        sortedResultList = sorted(resultList, key=operator.itemgetter(1), reverse=True)

        sortedResultList.insert(0, ("c2.symbol", "c0.score", "index", "c1.diseaseId"))

        pd.DataFrame.from_records(sortedResultList).to_csv(postIdMappingLocation + fname.split("/")[-1], index=False, header=False, quotechar='"', quoting=csv.QUOTE_ALL, sep='\t')