import configparser, glob

from disgenet.disgenet_python3 import main
from disgenet.findGeneNamesInData import findGeneNamesInData
from disgenet.interleaveTopGeneLists import interleaveTopGeneLists
from disgenet.mergeTopGeneLists import mergeTopGeneLists
from disgenet.selectTopGenesPerDisease import selectTopGenesPerDisease
import pandas as pd
import csv


def executePipeline():

    config, path, mergedTopGenesFileName, rankedGeneNameListFileName = readConfig()

    # retrieve gene disease associations for each disease and save in a separate file
    main("diseases_UMLS_codes.txt",config["dataLocations"]["geneDiseaseAssociationsLocation"], "disease", "cui")

    # select the top genes per disease that are either over a specified threshold or the top k and save in separate files
    selectTopGenesPerDisease(config['dataLocations']['geneDiseaseAssociationsLocation'],
                             config['selection'].getboolean("useThreshold"),
                             config['selection']['threshold'],
                             config['selection']['topK'])

    df = pd.read_csv(config["dataLocations"]["geneExpressionDataLocation"])

    if int(config['pipeline']['interleave']) == 2:

        # replace gene names in files from all the different diseases with the ones in the dataset
        for fname in glob.glob(path):

            newLocation = fname.split("/")
            newLocation[5] = "replaced"

            findGeneNamesInData(fname,
                                "/".join(newLocation),
                                df,
                                config["filtering"]["geneNameSeparator"])


        newPath = path.split("/")
        newPath[5] = "replaced"

        # interleave gene names from the different disease files
        results = interleaveTopGeneLists("/".join(newPath), mergedTopGenesFileName, True)

        saveResults(rankedGeneNameListFileName, results)

    else:

        if int(config['pipeline']['interleave']) == 0:
            # merge the top genes from different diseases into one list without duplicates
            mergeTopGeneLists(path, mergedTopGenesFileName,
                                    config['selection'].getboolean("useThreshold"),
                                    config['selection']['threshold'],
                                    config['selection']['topK'])

        elif int(config['pipeline']['interleave']) == 1:

            # interleave the gene names from the merged disease file
            interleaveTopGeneLists(path, mergedTopGenesFileName, False)

        # find top genes from disgenet in the gene expression data by matching names and save together with score and index
        findGeneNamesInData(mergedTopGenesFileName,
                        rankedGeneNameListFileName,
                        df,
                        config["filtering"]["geneNameSeparator"])


def readConfig():
    config = configparser.ConfigParser()
    config.read('config.ini')

    if config['selection'].getboolean("useThreshold"):

        path = "../../../data/disgenet/selectedThreshold" + str(config['selection']['threshold']) \
            .replace(".", "") + "/*.tsv"

        mergedTopGenesFileName = config['dataLocations']['mergedTopGenesLocation'] + "Threshold" + \
                                 str(config['selection']['threshold']).replace(".", "") + ".csv"

        rankedGeneNameListFileName = config["dataLocations"]["rankedGeneNameList"] + "Threshold" + \
                                     str(config['selection']['threshold']).replace(".", "") + ".csv"

    else:

        path = "../../../data/disgenet/selectedTop" + str(config['selection']['topK']) + "/*.tsv"

        mergedTopGenesFileName = config['dataLocations']['mergedTopGenesLocation'] + "Top" + \
                                 str(config['selection']['topK']) + ".csv"

        rankedGeneNameListFileName = config['dataLocations']['rankedGeneNameList'] + "Top" + \
                                     str(config['selection']['topK']) + ".csv"

    return config, path, mergedTopGenesFileName, rankedGeneNameListFileName


def saveResults(fileName, results):
    with open(fileName, "w") as csvfile:
        csvWriter = csv.writer(csvfile, quotechar='"', quoting=csv.QUOTE_ALL)

        csvWriter.writerow(["attributeName", "score", "index", "diseaseId"])

        for tup in results:

            csvWriter.writerow(list(tup))

if __name__ == '__main__':

    executePipeline()