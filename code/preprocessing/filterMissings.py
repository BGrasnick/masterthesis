import missingno as msno

import pandas as pd

def filterMissings(threshold, rawDataLocation, missingsFilteredLocation):

    df = pd.read_csv(rawDataLocation)

    # first filter out the genes that have more missings than threshold
    filtered_gene_data = msno.nullity_filter(df, filter = 'top', p = 1 - threshold)

    # second transpose matrix and filter out samples that have more missings than threshold
    filtered_gene_sample_data = msno.nullity_filter(filtered_gene_data.T, filter = 'top', p = 1 - threshold)

    # transpose back into original orientation and save
    filtered_gene_sample_data.T.to_csv(missingsFilteredLocation, index=False)