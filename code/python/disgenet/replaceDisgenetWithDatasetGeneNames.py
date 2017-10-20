import pandas as pd
import csv

def replaceDisgenetWithDatasetGeneNames(topGeneList, genesWithReplacedNamesLocation, df, geneNameSeparator):

    # get the header and add index as this is used later in the evaluation for filtering genes out from the dataset
    header = ("attributeName", "score", "index", "diseaseId")

    # list which is later saved as our final result, add header to it
    genesWithNameReplaced = [header]

    # this can be used for checking how many genes were found per disgenet name
    genesWithNumberOfFound = []

    # used for checking if a gene was found multiple times
    genesAdded = set()

    for tup in topGeneList:

        # get the genes that exactly match the name (minus the separator | and the number)
        matching = [geneName for geneName in df.columns if geneName.split(geneNameSeparator)[0] == tup[0]]

        # if we didn't find an exact match, look for subtypes
        if len(matching) == 0:
            matching = [s for s in df.columns if s.startswith(tup[0])]

        genesWithNumberOfFound.append((tup[1], len(matching)))

        for match in matching:

            # check if the gene was already added
            # (the one with the biggest score will always be added first because of the sorting)
            if not match in genesAdded:

                # add gene name, score and index to our final list
                genesWithNameReplaced.append((match, tup[1], df.columns.get_loc(match) - 1, tup[2]))

                genesAdded.add(match)

    pd.DataFrame.from_records(genesWithNameReplaced).to_csv(genesWithReplacedNamesLocation, index=False, header=False, quotechar='"', quoting=csv.QUOTE_ALL)