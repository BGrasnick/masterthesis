import missingno as msno

import pandas as pd

import gc

threshold = 0.1

df = pd.read_csv("../../data/transposed_final.csv")

filtered_gene_data = msno.nullity_filter(df, filter = 'top', p = 1 - threshold)

filtered_gene_sample_data = msno.nullity_filter(filtered_gene_data.T, filter = 'top', p = 1 - threshold)

filtered_gene_sample_data.T.to_csv("../../data/filtered.csv", index=False)