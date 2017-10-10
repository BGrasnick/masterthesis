import pandas as pd
import glob, os

def selectTopGenesPerDisease(geneDiseaseAssociationsLocation, useThreshold, threshold, topK):

    path = geneDiseaseAssociationsLocation + "*.tsv"

    # loop through all files in the gene disease assocation location
    for fname in glob.glob(path):
        df = pd.read_csv(fname, sep='\t')
        df.sort_values('c0.score', ascending = False)

        # split by directories in order to put results in new directory
        newNameList = fname.split("/")

        # filter using either a threshold or a topK approach
        if useThreshold:
            # add selectThreshold and the threshold as a directory
            newNameList.insert(-1,'selectedThreshold'  + str(threshold).replace(".",""))
            newName = "/".join(newNameList)

            # create directory if not already existing
            if not os.path.isdir("/".join(newNameList[0:-1])):
                os.makedirs("/".join(newNameList[0:-1]))

            # filter entries using the threshold and save
            df[df["c0.score"] >= float(threshold)][["c1.diseaseId", "c2.symbol", "c0.score"]].to_csv(newName)

        else:
            # add selectTop and the k as a directory
            newNameList.insert(-1,'selectedTop' + str(topK))
            newName = "/".join(newNameList)

            # create directory if not already existing
            if not os.path.isdir("/".join(newNameList[0:-1])):
                os.makedirs("/".join(newNameList[0:-1]))

            # only retain the top k entries and save
            df[0:int(topK)][["c1.diseaseId", "c2.symbol", "c0.score"]].to_csv(newName)

