# coding: utf-8
import pandas as pd

def transpose(sourceDataLocation, rawDataLocation):

    df = pd.read_csv(sourceDataLocation, sep="\t", header=None, names=range(3603))
    dfT = df.T
    dfT[0][0] = "cancer_type"
    dfT[1][0] = "patient_ID"
    dfT.to_csv(rawDataLocation, index=False, header=False)
