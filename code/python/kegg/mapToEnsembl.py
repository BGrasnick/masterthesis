from utils import writeSetToFile

from disgenet.utils import loadUniProtToEnsemblMap

def mapToEnsembl(geneIdListLocation, ensemblIdListLocation):

    uniprotKEGGMap = loadUniProtToEnsemblMap("../../../data/disgenet/HUMAN_9606_idmapping.dat/uniprotToKEGG_swapped.tsv")
    uniprotEnsemblMap = loadUniProtToEnsemblMap("../../../data/disgenet/HUMAN_9606_idmapping.dat/uniprotToEnsembl.tsv")

    geneIdList = [line.rstrip() for line in open(geneIdListLocation)]

    ensemblGeneList = []

    for geneId in geneIdList:
        if geneId.strip() in uniprotKEGGMap.keys():
            uniprotIds = uniprotKEGGMap[geneId.strip()]
            for uniprotId in uniprotIds:
                if uniprotId in uniprotEnsemblMap.keys():
                    ensemblGeneList.extend(uniprotEnsemblMap[uniprotId])

    writeSetToFile(set(ensemblGeneList), ensemblIdListLocation)