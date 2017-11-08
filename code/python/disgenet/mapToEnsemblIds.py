from urllib.parse import urlencode
from urllib.request import urlopen, Request
import glob, pdb
import pandas as pd
from collections import defaultdict


def mapToEnsemblIds(geneDiseaseAssociationsLocation):

    path = geneDiseaseAssociationsLocation + "*.tsv"

    for fname in glob.glob(path):
        df = pd.read_csv(fname, sep='\t')

        geneUniprotIDList = df["c2.uniprotId"].tolist()

        url = 'http://www.uniprot.org/uploadlists/'

        params = {
            'from': 'ACC',
            'to': 'ENSEMBL_ID',
            'format': 'tab',
            'query': " ".join(geneUniprotIDList)}

        data = urlencode(params).encode("utf-8")
        request = Request(url, data)
        request.add_header('User-Agent', 'Python')
        response = urlopen(request)
        page = response.read(200000)

        df_times = df["c2.uniprotId"].str.count(";") + 1

        df["df_times"] = df_times

        df = df.loc[df.index.repeat(df.df_times)].reset_index()

        lastName = ""
        lastIdx = 0

        for index, elem in df.iterrows():

            if elem["df_times"] > 1:
                if lastName != elem["c2.symbol"]:
                    lastName = elem["c2.symbol"]
                    lastIdx = 0

                df.set_value(index, "c2.uniprotId", elem["c2.uniprotId"].split(";")[lastIdx].replace(".",""))
                lastIdx += 1

        uniProtEnsemblDict = defaultdict()

        for entry in page.decode("utf-8").split("\n")[1:]:

            if entry:
                uniprot, ensembl = entry.split("\t")
                uniProtEnsemblDict[uniprot] = ensembl

        indexes_to_drop = []

        for index, elem in df.iterrows():
            if elem["c2.uniprotId"] in uniProtEnsemblDict.keys():
                df.set_value(index, "c2.symbol", uniProtEnsemblDict[elem["c2.uniprotId"]])
            else:
                df.set_value(index, "c2.symbol", "")
                indexes_to_drop.append(index)

        indexes_to_keep = set(range(df.shape[0])) - set(indexes_to_drop)
        df = df.take(list(indexes_to_keep))

        df.to_csv(fname,  index=False, sep="\t")
