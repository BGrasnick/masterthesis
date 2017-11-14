import pandas as pd
import os
from utils import createOrClearDirectory

def selectTopGenesPerDisease(postIdMappingLocation, selectedGenesPath, useThreshold, threshold, topK):

    # loop through all files in the gene disease assocation location
    for fname in os.listdir(postIdMappingLocation):

        df = pd.read_csv(os.path.join(postIdMappingLocation, fname), sep='\t')

        df.sort_values('c0.score', ascending = False)

        # split by directories in order to put results in new directory
        newName = selectedGenesPath + fname.split("/")[-1]

        createOrClearDirectory("/".join(newName.split("/")[:-1]))

        # filter using either a threshold or a topK approach
        if useThreshold:
            # filter entries using the threshold and save
            df[df["c0.score"] >= float(threshold)].to_csv(newName, index=False)

        else:
            # only retain the top k entries and save
            df[0:int(topK)].to_csv(newName, index=False)

