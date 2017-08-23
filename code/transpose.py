# coding: utf-8
import pandas as pd
import numpy as np

df = pd.read_csv("../data/PanCan12.3602-corrected-v3.csv", sep="\t", header=None, names=range(3603))
dfT = df.T
dfT[0][0] = "cancer type"
dfT[1][0] = "patient ID"
dfT.to_csv("../data/transposed_final.csv", index=False, header=False)
