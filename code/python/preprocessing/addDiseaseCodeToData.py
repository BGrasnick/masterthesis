import pandas as pd

def addDiseaseCodeToData(dataFileLocation, diseaseCodeFileLocation, outputLocation):

    df = pd.read_csv(dataFileLocation)
    diseaseCodes = pd.read_csv(diseaseCodeFileLocation)

    diseaseColumn = []

    for i in range(len(df[df.columns[0]])):
        diseaseColumn.append(diseaseCodes[df[df.columns[0]][i]][0])

    df.insert(0, column="diseaseCode", value=diseaseColumn)

    df_without_missings = df.dropna(subset = ['diseaseCode'])

    df_without_missings.to_csv(outputLocation, index=False)