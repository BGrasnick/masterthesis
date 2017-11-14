import configparser, time

from disgenet_python3 import main
from mapToEnsemblIds import mapToEnsemblIds
from mapToTCGAIds import mapToTCGAIds
from interleaveGeneLists import interleaveGeneLists
from mergeTopGeneLists import mergeTopGeneLists
from selectTopGenesPerDisease import selectTopGenesPerDisease
import csv, sys

def executePipeline():

    config, selectedGenesPath, mergedTopGenesLocation, genesWithReplacedNamesLocation = readConfig()

    featureNames = loadFeatureNames(config["dataLocations"]["geneExpressionDataLocation"])

    if config["pipeline"]["dataset"] == "GDC":
        uniProtToEnsemblMap = loadUniProtToEnsemblMap(config["dataLocations"]["uniprotToEnsemblMapLocation"])

    begin_timestamp = time.time()

    # retrieve gene disease associations for each disease and save in a separate file
    main(config["dataLocations"]["disgenetDiseaseCodesLocation"], config["dataLocations"]["geneDiseaseAssociationsLocation"], "disease", "cui")

    postfetching_timestamp = time.time()

    print("fetching time: %f" % (postfetching_timestamp - begin_timestamp))

    if config["pipeline"]["dataset"] == "GDC":

        mapToEnsemblIds(config['dataLocations']['geneDiseaseAssociationsLocation'], config["dataLocations"]["postIdMappingLocation"], uniProtToEnsemblMap, featureNames)

    elif config["pipeline"]["dataset"] == "TCGA":

        mapToTCGAIds(config['dataLocations']['geneDiseaseAssociationsLocation'],
                     config["dataLocations"]["postIdMappingLocation"], featureNames,
                     config["filtering"]["geneNameSeparator"], config['selection'].getboolean("useThreshold"),
                     config['selection']['threshold'], config['selection']['topK'])

    mapping_timestamp = time.time()

    print("mapping ensembl Ids time: %f" % (mapping_timestamp - postfetching_timestamp))

    # select the top genes per disease that are either over a specified threshold or the top k and save in separate files
    selectTopGenesPerDisease(config['dataLocations']['postIdMappingLocation'],
                             selectedGenesPath,
                             config['selection'].getboolean("useThreshold"),
                             config['selection']['threshold'],
                             config['selection']['topK'])

    topSelection_timestamp = time.time()

    print("selecting top genes time: %f" % (topSelection_timestamp - mapping_timestamp))

    if int(config['pipeline']['interleave']) == 2:

        # interleave gene names from the different disease files
        interleavedTopGeneList = interleaveGeneLists(selectedGenesPath)

        interleave_timestamp = time.time()

        print("interleaved gene names time: %f" % (interleave_timestamp - topSelection_timestamp))

        end_timestamp = time.time()

        print("total elapsed time: %f" % (end_timestamp - begin_timestamp))

        saveTupleList(genesWithReplacedNamesLocation, interleavedTopGeneList)

    else:

        # merge the top genes from different diseases into one list without duplicates
        topGeneList = mergeTopGeneLists(selectedGenesPath, config['selection'].getboolean("useThreshold"),
                                        config['selection']['threshold'],
                                        config['selection']['topK'])

        merge_timestamp = time.time()

        print("merge gene names time: %f" % (merge_timestamp - topSelection_timestamp))

        end_timestamp = time.time()

        print("total elapsed time: %f" % (end_timestamp - begin_timestamp))

        saveTupleList(genesWithReplacedNamesLocation, topGeneList)

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

def readConfig():
    config = configparser.ConfigParser()
    config.read('config.ini')

    if config['selection'].getboolean("useThreshold"):

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

    return config, selectedGenesPath, mergedTopGenesLocation, genesWithReplacedNamesLocation

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

if __name__ == '__main__':

    executePipeline()
