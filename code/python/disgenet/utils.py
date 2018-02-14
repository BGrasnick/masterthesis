import configparser
import os, csv, sys

def createOrClearDirectory(directoryLocation):
    # create directory if not already existing
    if not os.path.isdir(directoryLocation):
        os.makedirs(directoryLocation)
    else:
        for file in os.listdir(directoryLocation):
            os.remove(os.path.join(directoryLocation,file))

def loadUniProtToEnsemblMap(uniprotToEnsemblMapLocation):
    uniprotToEnsemblMap = dict()
    with open(uniprotToEnsemblMapLocation, 'r') as csvfile:
        uniProtToEnsemblReader = csv.reader(csvfile, delimiter='\t')
        for uniprot, ensembl, ensemblId in uniProtToEnsemblReader:
            if uniprot in uniprotToEnsemblMap.keys():
                uniprotToEnsemblMap[uniprot].append(ensemblId)
            else:
                uniprotToEnsemblMap[uniprot] = [ensemblId]

    return uniprotToEnsemblMap

def loadFeatureNames(geneExpressionDataLocation):

    csv.field_size_limit(sys.maxsize)

    with open(geneExpressionDataLocation, 'r') as csvfile:
        geneExpressionDataReader = csv.reader(csvfile, delimiter=',')
        featureNames = next(geneExpressionDataReader)

    return featureNames

def createLocationsFromConfig(config):

    if config['selection']["useThreshold"]:

        selectedGenesPath = "../../../data/disgenet/selectedThreshold" + str(config['selection']['threshold']) \
            .replace(".", "") + "/"

        mergedTopGenesLocation = config['dataLocations']['mergedTopGenesLocation'] + "Threshold" + \
                                 str(config['selection']['threshold']).replace(".", "") + ".csv"

        genesWithReplacedNamesLocation = config["dataLocations"]["rankedGeneNameList"] + "Threshold" + \
                                     str(config['selection']['threshold']).replace(".", "") + ".csv"

    else:

        selectedGenesPath = "../../../data/disgenet/selectedTop" + str(config['selection']['topK']) + "/"

        mergedTopGenesLocation = config['dataLocations']['mergedTopGenesLocation'] + "Top" + \
                                 str(config['selection']['topK']) + ".csv"

        genesWithReplacedNamesLocation = config['dataLocations']['rankedGeneNameList'] + "Top" + \
                                     str(config['selection']['topK']) + ".csv"

    return selectedGenesPath, mergedTopGenesLocation, genesWithReplacedNamesLocation

def saveTupleList(fileName, tupleList):
    with open(fileName, "w") as csvfile:
        csvWriter = csv.writer(csvfile, quotechar='"', quoting=csv.QUOTE_ALL)

        csvWriter.writerow(["attributeName", "score", "index", "diseaseId"])

        for tup in tupleList:

            csvWriter.writerow(list(tup))

def loadTupleList(fileName):

    with open(fileName, "r") as csvfile:
        csvReader = csv.reader(csvfile, quotechar='"', quoting=csv.QUOTE_ALL)
        tupleList = [tuple(line) for line in csvReader]

    return tupleList