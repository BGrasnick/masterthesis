import pandas as pd
import glob, os

def selectTopGenesPerDisease(geneDiseaseAssociationsLocation, useThreshold, threshold, topK):

    path = geneDiseaseAssociationsLocation + "*.tsv"

    for fname in glob.glob(path):
        df = pd.read_csv(fname, sep='\t')
        df.sort_values('c0.score', ascending = False)

        newNameList = fname.split("/")

        if useThreshold:
            newNameList.insert(-1,'selectedTreshold'  + str(threshold).replace(".",""))
            newName = "/".join(newNameList)
            if not os.path.isdir("/".join(newNameList[0:-1])):
                os.makedirs("/".join(newNameList[0:-1]))
            df[df["c0.score"] >= float(threshold)][["c1.diseaseId", "c2.symbol", "c0.score"]].to_csv(newName)
        else:
            newNameList.insert(-1,'selectedTop' + str(topK))
            newName = "/".join(newNameList)
            if not os.path.isdir("/".join(newNameList[0:-1])):
                os.makedirs("/".join(newNameList[0:-1]))
            df[0:int(topK)][["c1.diseaseId", "c2.symbol", "c0.score"]].to_csv(newName)

