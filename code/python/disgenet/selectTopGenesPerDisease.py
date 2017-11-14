import pandas as pd
import os

def selectTopGenesPerDisease(postIdMappingLocation, selectedGenesPath, useThreshold, threshold, topK):

    # loop through all files in the gene disease assocation location
    for fname in os.listdir(postIdMappingLocation):

        df = pd.read_csv(os.path.join(postIdMappingLocation, fname), sep='\t')

        df.sort_values('c0.score', ascending = False)

        # split by directories in order to put results in new directory
        newName = selectedGenesPath + fname.split("/")[-1]

        # filter using either a threshold or a topK approach
        if useThreshold:

            # create directory if not already existing
            if not os.path.isdir("/".join(newName.split("/")[:-1])):
                os.makedirs("/".join(newName.split("/")[:-1]))

            # filter entries using the threshold and save
            df[df["c0.score"] >= float(threshold)].to_csv(newName, index=False)

        else:

            # create directory if not already existing
            if not os.path.isdir("/".join(newName.split("/")[:-1])):
                os.makedirs("/".join(newName.split("/")[:-1]))

            # only retain the top k entries and save
            df[0:int(topK)].to_csv(newName, index=False)

