import configparser, glob, time

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

    begin_timestamp = time.time()

    # retrieve gene disease associations for each disease and save in a separate file
    main(config["dataLocations"]["disgenetDiseaseCodesLocation"],config["dataLocations"]["geneDiseaseAssociationsLocation"], "disease", "cui")

    mapToEnsemblIds(config['dataLocations']['geneDiseaseAssociationsLocation'])

    # select the top genes per disease that are either over a specified threshold or the top k and save in separate files
    selectTopGenesPerDisease(config['dataLocations']['geneDiseaseAssociationsLocation'],
                             config['selection'].getboolean("useThreshold"),
                             config['selection']['threshold'],
                             config['selection']['topK'])

    if int(config['pipeline']['interleave']) == 2:

        # replace gene names in files from all the different diseases with the ones in the dataset
        for fname in glob.glob(path):

            # put in single files in folder replaced to use later on for interleaving
            newLocation = fname.split("/")
            newLocation[5] = "replaced"

            tupleList = loadTupleList(fname)

            # get rid of the header
            tupleList.pop(0)

            replaceDisgenetWithDatasetGeneNames(tupleList, "/".join(newLocation), df, config["filtering"]["geneNameSeparator"])

        # load single files in folder replaced for interleaving
        newPath = path.split("/")
        newPath[5] = "replaced"

        # interleave gene names from the different disease files
        interleavedTopGeneList = interleaveGeneLists("/".join(newPath))

        saveTupleList(genesWithReplacedNamesLocation, interleavedTopGeneList)

        end_timestamp = time.time()

        print("elapsed time: %f" % (end_timestamp - begin_timestamp))

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