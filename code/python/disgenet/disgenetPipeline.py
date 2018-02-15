import time

from disgenet.disgenet_python3 import main
from disgenet.mapToEnsemblIds import mapToEnsemblIds
from disgenet.mapToTCGAIds import mapToTCGAIds
from disgenet.interleaveGeneLists import interleaveGeneLists
from disgenet.mergeTopGeneLists import mergeTopGeneLists
from disgenet.selectTopGenesPerDisease import selectTopGenesPerDisease
from disgenet.utils import createOrClearDirectory, loadUniProtToEnsemblMap, loadFeatureNames, createLocationsFromConfig, saveTupleList


def executeDisgenetPipeline(config, geneExpressionDataLocation, resultsLocation, geneNameSeparator, uniprotToEnsemblMapLocation):

    selectedGenesPath, mergedTopGenesLocation = createLocationsFromConfig(config)

    featureNames = loadFeatureNames(geneExpressionDataLocation)

    if config["pipeline"]["dataset"] == "GDC":
        uniProtToEnsemblMap = loadUniProtToEnsemblMap(uniprotToEnsemblMapLocation)

    begin_timestamp = time.time()

    # retrieve gene disease associations for each disease and save in a separate file
    createOrClearDirectory(config["dataLocations"]["geneDiseaseAssociationsLocation"])
    main(config["dataLocations"]["disgenetDiseaseCodesLocation"], config["dataLocations"]["geneDiseaseAssociationsLocation"], "disease", "cui")

    #postfetching_timestamp = time.time()

    #print("fetching time: %f" % (postfetching_timestamp - begin_timestamp))

    if config["pipeline"]["dataset"] == "GDC":

        mapToEnsemblIds(config['dataLocations']['geneDiseaseAssociationsLocation'],
                        config["dataLocations"]["postIdMappingLocation"], uniProtToEnsemblMap,
                        featureNames, config["pipeline"]["useAllUniprotIds"], config["pipeline"]["useAllEnsemblIds"])

    elif config["pipeline"]["dataset"] == "TCGA":

        mapToTCGAIds(config['dataLocations']['geneDiseaseAssociationsLocation'],
                     config["dataLocations"]["postIdMappingLocation"], featureNames,
                     geneNameSeparator, config['selection']["useThreshold"],
                     config['selection']['threshold'], config['selection']['topK'])

    #mapping_timestamp = time.time()

    #print("mapping ensembl Ids time: %f" % (mapping_timestamp - postfetching_timestamp))

    # select the top genes per disease that are either over a specified threshold or the top k and save in separate files
    selectTopGenesPerDisease(config['dataLocations']['postIdMappingLocation'],
                             selectedGenesPath,
                             config['selection']["useThreshold"],
                             config['selection']['threshold'],
                             config['selection']['topK'])

    #topSelection_timestamp = time.time()

    #print("selecting top genes time: %f" % (topSelection_timestamp - mapping_timestamp))

    if int(config['pipeline']['interleave']) == 2:

        # interleave gene names from the different disease files
        interleavedTopGeneList = interleaveGeneLists(selectedGenesPath)

        #interleave_timestamp = time.time()

        #print("interleaved gene names time: %f" % (interleave_timestamp - topSelection_timestamp))

        end_timestamp = time.time()

        print("total elapsed time: %f" % (end_timestamp - begin_timestamp))

        saveTupleList(resultsLocation + "disgenet.csv", interleavedTopGeneList)

    else:

        # merge the top genes from different diseases into one list without duplicates
        topGeneList = mergeTopGeneLists(selectedGenesPath, config['selection'].getboolean("useThreshold"),
                                        config['selection']['threshold'],
                                        config['selection']['topK'])

        #merge_timestamp = time.time()

        #print("merge gene names time: %f" % (merge_timestamp - topSelection_timestamp))

        end_timestamp = time.time()

        print("total elapsed time: %f" % (end_timestamp - begin_timestamp))

        saveTupleList(resultsLocation + "disgenet.csv", topGeneList)

if __name__ == '__main__':

    executeDisgenetPipeline()
