# coding: utf-8
import pandas as pd

def discretize(inputDataLocation, outputDataLocation):

	df = pd.read_csv(inputDataLocation, header=0)

	discretized_df = pd.DataFrame()

	# take over cancer_type and patient_ID to discretized datafame
	discretized_df[df.columns[0]] = df[df.columns[0]]
	discretized_df[df.columns[1]] = df[df.columns[1]]

	# just for logging
	i = 3
	numberOfColums = len(df.columns)

	# loop over all gene expression columns (excluding cancer_type and patient_ID
	for columnName in df.columns[2:]:

		print("Discretizing " + str(i) + "/" + str(numberOfColums) + "\t -> " + str(columnName))

		column = df[columnName]

		# calculate min and max for the bin borders
		minimum, maximum = column.min(), column.max()

		# in case mean - std/2 is less than minimum, decrease minimum a tiny bit
		if column.mean() - column.std()/2 < minimum:
			minimum = column.mean() - column.std()/1.99

		# in case mean + std/2 is more than maximum, increase maximum a tiny bit
		if column.mean() + column.std()/2 > maximum:
			maximum = column.mean() + column.std()/1.99

		# list of the borders where to change from on bin from another (4 borders for 3 bins) | bin | bin | bin |
		bins = [minimum, column.mean() - column.std()/2, column.mean() + column.std()/2, maximum]

		# cuts the continuous data into the 3 bins with labels -1, 0 and 1
		discretized = pd.cut(column, bins, labels=[-1,0,1])
		discretized_df[columnName] = discretized

		i += 1

	discretized_df.to_csv(outputDataLocation, index=False)