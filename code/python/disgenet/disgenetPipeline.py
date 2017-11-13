import configparser, glob, time

from disgenet.addDatasetIndicesToDisgenetGenes import addDatasetIndicesToDisgenetGenes
from disgenet.disgenet_python3 import main
from disgenet.mapToEnsemblIds import mapToEnsemblIds
from disgenet.replaceDisgenetWithDatasetGeneNames import replaceDisgenetWithDatasetGeneNames
from disgenet.interleaveGeneLists import interleaveGeneLists
from disgenet.mergeTopGeneLists import mergeTopGeneLists
from disgenet.selectTopGenesPerDisease import selectTopGenesPerDisease
import pandas as pd
import csv

def executePipeline():

    config, path, mergedTopGenesLocation, genesWithReplacedNamesLocation = readConfig()

    df = pd.read_csv(config["dataLocations"]["geneExpressionDataLocation"])

    uniProtToEnsemblMap = loadUniProtToEnsemblMap(config["dataLocations"]["uniprotToEnsemblMapLocation"])

    begin_timestamp = time.time()

    # retrieve gene disease associations for each disease and save in a separate file
    main(config["dataLocations"]["disgenetDiseaseCodesLocation"],config["dataLocations"]["geneDiseaseAssociationsLocation"], "disease", "cui")

    postfetching_timestamp = time.time()

    print("fetching time: %f" % (postfetching_timestamp - begin_timestamp))

    if config["pipeline"]["dataset"] == "GDC":

        mapToEnsemblIds(config['dataLocations']['geneDiseaseAssociationsLocation'], uniProtToEnsemblMap)

        mapping_timestamp = time.time()

        print("mapping ensembl Ids time: %f" % (mapping_timestamp - postfetching_timestamp))

    # select the top genes per disease that are either over a specified threshold or the top k and save in separate files
    selectTopGenesPerDisease(config['dataLocations']['geneDiseaseAssociationsLocation'],
                             config['selection'].getboolean("useThreshold"),
                             config['selection']['threshold'],
                             config['selection']['topK'])

    topSelection_timestamp = time.time()

    if config["pipeline"]["dataset"] == "GDC":
        print("selecting top genes time: %f" % (topSelection_timestamp - mapping_timestamp))

        for fname in glob.glob(path):
            tupleList = loadTupleList(fname)
            newTupleList = addDatasetIndicesToDisgenetGenes(tupleList, df)
            saveTupleList(newTupleList, fname)

        addingIndices_timestamp = time.time()

        print("adding indices time: %f" % (addingIndices_timestamp - topSelection_timestamp))

    else:
        print("selecting top genes time: %f" % (topSelection_timestamp - postfetching_timestamp))

    if int(config['pipeline']['interleave']) == 2:

        if config["pipeline"]["dataset"] == "TCGA":

            # replace gene names in files from all the different diseases with the ones in the dataset
            for fname in glob.glob(path):

                    # put in single files in folder replaced to use later on for interleaving
                    newLocation = fname.split("/")
                    newLocation[5] = "replaced"

                    tupleList = loadTupleList(fname)

                    # get rid of the header
                    tupleList.pop(0)

                    replaceDisgenetWithDatasetGeneNames(tupleList, "/".join(newLocation), df, config["filtering"]["geneNameSeparator"])

            geneNameReplacement_timestamp = time.time()

            print("replaced gene names time: %f" % (geneNameReplacement_timestamp - topSelection_timestamp))

            # load single files in folder replaced for interleaving
            newPath = path.split("/")
            newPath[5] = "replaced"

            # interleave gene names from the different disease files
            interleavedTopGeneList = interleaveGeneLists("/".join(newPath))

            interleave_timestamp = time.time()

            print("interleaved gene names time: %f" % (interleave_timestamp - geneNameReplacement_timestamp))

        else:
            # interleave gene names from the different disease files
            interleavedTopGeneList = interleaveGeneLists(path)

            interleave_timestamp = time.time()

            print("interleaved gene names time: %f" % (interleave_timestamp - addingIndices_timestamp))

        saveTupleList(genesWithReplacedNamesLocation, interleavedTopGeneList)

        end_timestamp = time.time()

        print("total elapsed time: %f" % (end_timestamp - begin_timestamp))

    else:

        topGeneList = []

        if int(config['pipeline']['interleave']) == 0:
            # merge the top genes from different diseases into one list without duplicates
            topGeneList = mergeTopGeneLists(path, config['selection'].getboolean("useThreshold"),
                                    config['selection']['threshold'],
                                    config['selection']['topK'])

        elif int(config['pipeline']['interleave']) == 1:

            # interleave the gene names from the merged disease file
            topGeneList = interleaveGeneLists(path)

        # find top genes from disgenet in the gene expression data by matching names and save together with score and index
        replaceDisgenetWithDatasetGeneNames(topGeneList, genesWithReplacedNamesLocation, df, config["filtering"]["geneNameSeparator"])

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

def readConfig():
    config = configparser.ConfigParser()
    config.read('config.ini')

    if config['selection'].getboolean("useThreshold"):

        path = "../../../data/disgenet/selectedThreshold" + str(config['selection']['threshold']) \
            .replace(".", "") + "/*.tsv"

        mergedTopGenesLocation = config['dataLocations']['mergedTopGenesLocation'] + "Threshold" + \
                                 str(config['selection']['threshold']).replace(".", "") + ".csv"

        genesWithReplacedNamesLocation = config["dataLocations"]["rankedGeneNameList"] + "Threshold" + \
                                     str(config['selection']['threshold']).replace(".", "") + ".csv"

    else:

        path = "../../../data/disgenet/selectedTop" + str(config['selection']['topK']) + "/*.tsv"

        mergedTopGenesLocation = config['dataLocations']['mergedTopGenesLocation'] + "Top" + \
                                 str(config['selection']['topK']) + ".csv"

        genesWithReplacedNamesLocation = config['dataLocations']['rankedGeneNameList'] + "Top" + \
                                     str(config['selection']['topK']) + ".csv"

    return config, path, mergedTopGenesLocation, genesWithReplacedNamesLocation


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