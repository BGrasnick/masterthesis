import pandas as pd

def filterByDisgenetGenes(geneListLocation, dataLocation, outputLocation, geneNameSeparator):
    geneList = pd.read_csv(geneListLocation, header=None)

    df = pd.read_csv(dataLocation)

    allGenes = set()

    # add column cancer_type
    allGenes.add(df.columns[0])

    # this can be used for checking how many genes were found per disgenet name
    genesWithNumberOfFound = []

    for gene in geneList[0]:
        matching = [geneName for geneName in df.columns if geneName.split(geneNameSeparator)[0] == gene]

        # if we didn't find an exact match, look for subtypes
        if len(matching) == 0:
            matching = [s for s in df.columns if s.startswith(gene)]

        genesWithNumberOfFound.append((gene, len(matching)))
        allGenes.update(matching)

    # filter the data so only columns with disgenet gene names remain
    filtered_df = df.filter(allGenes)

    filtered_df.to_csv(outputLocation, index=False)



