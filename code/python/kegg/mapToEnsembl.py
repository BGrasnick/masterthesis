from kegg.utils import writeSetToFile

from disgenet.utils import loadUniProtToEnsemblMap

def mapToEnsembl(geneIdListLocation, ensemblIdListLocation, KEGGtoUniprotLocation, uniprotToEnsemblLocation):

    uniprotKEGGMap = loadUniProtToEnsemblMap(KEGGtoUniprotLocation)
    uniprotEnsemblMap = loadUniProtToEnsemblMap(uniprotToEnsemblLocation)

    geneIdList = [line.rstrip() for line in open(geneIdListLocation)]

    ensemblGeneList = []

    for geneId in geneIdList:
        if geneId.strip() in uniprotKEGGMap.keys():
            uniprotIds = uniprotKEGGMap[geneId.strip()]
            for uniprotId in uniprotIds:
                if uniprotId in uniprotEnsemblMap.keys():
                    ensemblGeneList.extend(uniprotEnsemblMap[uniprotId])

    writeSetToFile(set(ensemblGeneList), ensemblIdListLocation)