import pandas as pd

def filterByDisgenetGenes(geneListLocation, dataLocation, outputLocation, geneNameSeparator):
	geneList = pd.read_csv(geneListLocation, header=None)

	df = pd.read_csv(dataLocation)

	allGenes = set()
	allGenes.add(df.columns[0])
	genesWithNumberOfFound = []

	for gene in geneList[0]:
	    matching = [s for s in df.columns if s.split(geneNameSeparator)[0] == gene]
	    if len(matching) == 0:
	        matching = [s for s in df.columns if s.startswith(gene)]
	    genesWithNumberOfFound.append((gene,len(matching)))
	    allGenes.update(matching)

	filtered_df = df.filter(allGenes)

	filtered_df.to_csv(outputLocation, index=False)

filterByDisgenetGenes("../../data/disgenet/mergedList.csv", "../../data/transposed_final.csv", "../../data/filteredByDisgenetGenes.csv", "|")