import glob, pdb
import pandas as pd
from collections import defaultdict


def mapToEnsemblIds(geneDiseaseAssociationsLocation, uniProtToEnsemblMap):

    path = geneDiseaseAssociationsLocation + "*.tsv"

    for fname in glob.glob(path):
        df = pd.read_csv(fname, sep='\t')

        df_times = df["c2.uniprotId"].str.count(";") + 1

        df["df_times"] = df_times

        df = df.loc[df.index.repeat(df.df_times)].reset_index()

        lastName = ""
        lastIdx = 0

        for index, elem in df.iterrows():

            if elem["df_times"] > 1:
                if lastName != elem["c2.symbol"]:
                    lastName = elem["c2.symbol"]
                    lastIdx = 0

                    df.at[index,"c2.symbol"] = elem["c2.uniprotId"].split(";")[lastIdx].replace(".","")
                lastIdx += 1

        indexes_to_drop = []

        for index, elem in df.iterrows():
            if elem["c2.uniprotId"] in uniProtToEnsemblMap.keys():
                df.at[index,"c2.symbol"] = uniProtToEnsemblMap[elem["c2.uniprotId"]][0]
            else:
                df.at[index,"c2.symbol"] = ""
                indexes_to_drop.append(index)

        indexes_to_keep = set(range(df.shape[0])) - set(indexes_to_drop)
        df = df.take(list(indexes_to_keep))

        df.to_csv(fname+"new",  index=False, sep="\t")
