import configparser

from disgenet.disgenet_python3 import main
from disgenet.filterDataByDisgenetGenes import filterByDisgenetGenes
from disgenet.mergeTopGeneLists import mergeTopGeneLists
from disgenet.selectTopGenesPerDisease import selectTopGenesPerDisease


def executePipeline():

    config = configparser.ConfigParser()
    config.read('config.ini')

    # retrieve gene disease associations for each disease and save in a separate file
    main("diseases_UMLS_codes.txt",config["dataLocations"]["geneDiseaseAssociationsLocation"], "disease", "cui")

    # select the top genes per disease that are either over a specified threshold or the top k and save in separate files
    selectTopGenesPerDisease(config['dataLocations']['geneDiseaseAssociationsLocation'],
                             config['selection'].getboolean("useThreshold"), config['selection']['threshold'],
                             config['selection']['topK'])

    if config['selection'].getboolean("useThreshold"):

        path = "../../data/disgenet/selectedThreshold" + str(config['selection']['threshold']).replace(".",
                                                                                                       "") + "/*.tsv"

    else:

        path = "../../data/disgenet/selectedTop" + str(config['selection']['topK']) + "/*.tsv"

    # merge the top genes from different diseases into one list without duplicates
    mergeTopGeneLists(path, config['dataLocations']['mergedTopGenesLocation'])

    # filter the gene expression data to only include the top genes
    filterByDisgenetGenes(config["dataLocations"]["mergedTopGenesLocation"],
                          config["dataLocations"]["geneExpressionDataLocation"],
                          config["dataLocations"]["filteredOutputLocation"], config["filtering"]["geneNameSeparator"])


if __name__ == '__main__':

    executePipeline()