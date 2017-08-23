# coding: utf-8
import pandas as pd
import numpy as np

df = pd.read_csv("./data/expressions_with_missings_filtered_01.csv", header=0)

discretized_df = pd.DataFrame()

discretized_df[df.columns[0]] = df[df.columns[0]]
discretized_df[df.columns[1]] = df[df.columns[1]]

i = 3

numberOfColums = len(df.columns)

for columnName in df.columns[2:]:

	print("Discretizing " + str(i) + "/" + str(numberOfColums) + "\t -> " + str(columnName))

	column = df[columnName]
	minimum, maximum = column.min(), column.max()

	if column.mean() - column.std()*2 < minimum:
		minimum = column.mean() - column.std()*2.01

	if column.mean() + column.std()*2 > maximum:
		maximum = column.mean() + column.std()*2.01

	bins = [minimum, column.mean() - column.std()*2, column.mean() + column.std()*2, maximum]

	discretized = pd.cut(column, bins, labels=[-1,0,1])
	discretized_df[columnName] = discretized

	i += 1

discretized_df.to_csv("./discretized.csv", index=False)