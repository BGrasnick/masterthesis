import pandas as pd
import os

rowVars = pd.read_csv("/home/basti/development/masterthesis/for_real/resultsFromVM/GDC/good/rankedAttributes/rowVars.csv")
infoGain = pd.read_csv("/home/basti/development/masterthesis/for_real/resultsFromVM/GDC/good/rankedAttributes/InfoGain.csv")

for file in os.listdir("./input"):
    Kegg = pd.read_csv(os.path.join("./input", file), header=None)

    rowVarsKegg = rowVars[rowVars['attributeName'].isin(Kegg[Kegg.columns[0]].tolist())]
    infoGainKegg = infoGain[infoGain['attributeName'].isin(Kegg[Kegg.columns[0]].tolist())]

    rowVarsKegg.to_csv(os.path.join("./results", file).replace(".txt","rowVars.csv"), index = False)
    infoGainKegg.to_csv(os.path.join("./results", file).replace(".txt","infoGain.csv"), index = False)