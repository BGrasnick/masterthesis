from utils import writeSetToFile

import requests

KEGG_REST_API_BASE_URL = "http://rest.kegg.jp/link/hsa/"

def fetchGenes(keggIdListLocation, geneIdListLocation):

    keggIdList = [line.rstrip() for line in open(keggIdListLocation)]

    geneSet = set()

    for keggId in keggIdList:

        r = requests.get(KEGG_REST_API_BASE_URL + keggId)

        for resultLine in r.text.split("\n"):
            if resultLine:
                geneSet.add(resultLine.split("\t")[1].split(":")[1])

    writeSetToFile(geneSet, geneIdListLocation)