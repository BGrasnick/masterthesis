import pandas as pd

df = pd.read_csv("../../../data/GDC/TCGA-PRAD_TCGA-OV_TCGA-COAD_TCGA-LUSC_TCGA-BRCA_TCGA-PAAD_TCGA-STAD_TCGA-CESC__GeneExpressionQuantification_TP_HTSeq-Counts.csv")
diseaseCodes = pd.read_csv("../../../data/GDC/TCGA-PRAD_TCGA-OV_TCGA-COAD_TCGA-LUSC_TCGA-BRCA_TCGA-PAAD_TCGA-STAD_TCGA-CESC__GeneExpressionQuantification_TP_HTSeq-Counts_metadata.csv")

diseaseColumn = []

for i in range(len(df[df.columns[0]])):
    diseaseColumn.append(diseaseCodes[df[df.columns[0]][i]][0])

df.insert(0, column="diseaseCode", value=diseaseColumn)

df_without_missings = df.dropna(subset = ['diseaseCode'])

df_without_missings.to_csv("../../../data/GDC/TCGA-PRAD_TCGA-OV_TCGA-COAD_TCGA-LUSC_TCGA-BRCA_TCGA-PAAD_TCGA-STAD_TCGA-CESC__GeneExpressionQuantification_TP_HTSeq-Counts_WithDiseaseCodes.csv", index=False)