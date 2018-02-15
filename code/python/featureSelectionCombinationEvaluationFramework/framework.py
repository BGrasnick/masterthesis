import json, subprocess, os

from combination.combinePipeline import executeCombinePipeline
from datasetReduction.reduceDataset import reduceDataset
from kegg.keggPipeline import executeKEGGPipeline
from preprocessing.addDiseaseCodeToData import addDiseaseCodeToData
from disgenet.disgenetPipeline import executeDisgenetPipeline

def executeFrameworkPipeline():

    jsonFile = open("../../config.json")

    jsonConfig = json.load(jsonFile)

    jsonFile.close()

    datasetLocation = jsonConfig["preprocessing"]["outputLocation"]

    #####################
    ### PREPROCESSING ###
    #####################

    #addDiseaseCodeToData(jsonConfig["preprocessing"]["dataFileLocation"], jsonConfig["preprocessing"]["diseaseCodeFileLocation"], datasetLocation)

    # FETCH KEGG GENES AND TRANSFORM TO ENSEMBL
    executeKEGGPipeline(jsonConfig["externalKnowledge"]["KEGG"], jsonConfig["externalKnowledge"]["uniprotToEnsemblMapLocation"])

    #########################
    ### FEATURE SELECTION ###
    #########################

    # DISGENET FEATURE SELECTION

    executeDisgenetPipeline(jsonConfig["externalKnowledge"]["disgenet"], datasetLocation, jsonConfig["featureSelection"]["resultsLocation"], jsonConfig["dataset"]["geneNameSeparator"], jsonConfig["externalKnowledge"]["uniprotToEnsemblMapLocation"])

    # OPTIONALLY REDUCE DATASET TO KEGG, DISGENET OR COMBINED GENES BEFORE COMPUTATIONAL FEATURE SELECTION

    if jsonConfig["externalKnowledge"]["reduceDatasetGenesTo"] != "None":
        reduceDataset(jsonConfig["externalKnowledge"], datasetLocation, jsonConfig["featureSelection"]["resultsLocation"])
        datasetLocation = jsonConfig["externalKnowledge"]["reducedDatasetLocation"]

    # VARIANCE BASED FEATURE SELECTION

    p = subprocess.Popen(["Rscript", "VarianceBasedFeatureSelection.R", os.path.abspath(datasetLocation),
                          os.path.abspath(jsonConfig["featureSelection"]["resultsLocation"] + "VB-FS.csv"), jsonConfig["dataset"]["geneNameSeparator"]], cwd="../../R")
    p.wait()

    # WEKA FEATURE SELECTION
    
    args = ["java", "-jar", "../Java/target/WEKA_FeatureSelector.jar", os.path.abspath(datasetLocation),
                          os.path.abspath(jsonConfig["featureSelection"]["resultsLocation"])]

    args.extend(jsonConfig["WEKA-FS"]["FS-methods"])

    p = subprocess.Popen(args, cwd="../../Java")
    p.wait()

    ###########################
    ### FEATURE COMBINATION ###
    ###########################

    # COMBINE KNOWLEDGE BASE AND COMPUTATIONAL FEATURE RANKINGS

    executeCombinePipeline(jsonConfig["combination"], jsonConfig["featureSelection"]["resultsLocation"], jsonConfig["externalKnowledge"]["KEGG"]["ensemblIdListLocation"])

    ##########################
    ### FEATURE EVALUATION ###
    ##########################

    args = ["java", "-jar", "../Java/target/WEKA_Evaluator.jar", os.path.abspath(datasetLocation),
            os.path.abspath(jsonConfig["featureSelection"]["resultsLocation"]),
            os.path.abspath(jsonConfig["evaluation"]["resultsLocation"]), str(jsonConfig["evaluation"]["topKmin"]),
            str(jsonConfig["evaluation"]["topKmax"])]

    p = subprocess.Popen(args, cwd="../../Java")

    p.wait()

if __name__ == '__main__':

    executeFrameworkPipeline()