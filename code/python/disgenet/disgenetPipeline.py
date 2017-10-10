import configparser

from disgenet.disgenet_python3 import main
from disgenet.findGeneNamesInData import findGeneNamesInData
from disgenet.mergeTopGeneLists import mergeTopGeneLists
from disgenet.selectTopGenesPerDisease import selectTopGenesPerDisease

def executePipeline():

    config, path, mergedTopGenesFileName, rankedGeneNameListFileName = readConfig()

    # retrieve gene disease associations for each disease and save in a separate file
    main("diseases_UMLS_codes.txt",config["dataLocations"]["geneDiseaseAssociationsLocation"], "disease", "cui")

    # select the top genes per disease that are either over a specified threshold or the top k and save in separate files
    selectTopGenesPerDisease(config['dataLocations']['geneDiseaseAssociationsLocation'],
                             config['selection'].getboolean("useThreshold"),
                             config['selection']['threshold'],
                             config['selection']['topK'])

    # merge the top genes from different diseases into one list without duplicates
    mergeTopGeneLists(path, mergedTopGenesFileName,
                            config['selection'].getboolean("useThreshold"),
                            config['selection']['threshold'],
                            config['selection']['topK'])

    # find top genes from disgenet in the gene expression data by matching names and save together with score and index
    findGeneNamesInData(mergedTopGenesFileName,
                        rankedGeneNameListFileName,
                        config["dataLocations"]["geneExpressionDataLocation"],
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

if __name__ == '__main__':

    executePipeline()