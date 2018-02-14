import json, subprocess, os

from combination.combinePipeline import executeCombinePipeline
from kegg.keggPipeline import executeKEGGPipeline
from preprocessing.addDiseaseCodeToData import addDiseaseCodeToData
from disgenet.disgenetPipeline import executeDisgenetPipeline

def executeFrameworkPipeline():

    jsonFile = open("../../config.json")

    jsonConfig = json.load(jsonFile)

    jsonFile.close()

    #####################
    ### PREPROCESSING ###
    #####################

    #addDiseaseCodeToData(jsonConfig["preprocessing"]["dataFileLocation"], jsonConfig["preprocessing"]["diseaseCodeFileLocation"], jsonConfig["preprocessing"]["outputLocation"])

    #########################
    ### FEATURE SELECTION ###
    #########################
    '''
    # DISGENET FEATURE SELECTION

    executeDisgenetPipeline(jsonConfig["disgenet"], jsonConfig["preprocessing"]["outputLocation"])

    # VARIANCE BASED FEATURE SELECTION

    p = subprocess.Popen(["Rscript", "VarianceBasedFeatureSelection.R", os.path.abspath(jsonConfig["preprocessing"]["outputLocation"]),
                          os.path.abspath(jsonConfig["VB-FS"]["featureRankingOutputLocation"]), jsonConfig["disgenet"]["filtering"]["geneNameSeparator"]], cwd="../../R")
    p.wait()

    # WEKA FEATURE SELECTION

    args = ["java", "-jar", "../Java/target/WEKA_FeatureSelector.jar", os.path.abspath(jsonConfig["preprocessing"]["outputLocation"]),
                          os.path.abspath(jsonConfig["WEKA-FS"]["featureRankingOutputLocation"])]

    args.extend(jsonConfig["WEKA-FS"]["FS-methods"])

    p = subprocess.Popen(args, cwd="../../Java")
    p.wait()

    ###########################
    ### FEATURE COMBINATION ###
    ###########################

    # FETCH KEGG GENES AND TRANSFORM TO ENSEMBL

    executeKEGGPipeline(jsonConfig["combination"]["KEGG"], jsonConfig["disgenet"]["uniprotToEnsemblMapLocation"])

    # COMBINE KNOWLEDGE BASE AND COMPUTATIONAL FEATURE RANKINGS

    executeCombinePipeline(jsonConfig)
    
    '''

    ##########################
    ### FEATURE EVALUATION ###
    ##########################

    args = ["java", "-jar", "../Java/target/WEKA_Evaluator.jar", os.path.abspath(jsonConfig["preprocessing"]["outputLocation"]),
            os.path.abspath(jsonConfig["combination"]["resultsLocation"]),
            os.path.abspath(jsonConfig["evaluation"]["resultsLocation"]), str(jsonConfig["evaluation"]["topKmin"]),
            str(jsonConfig["evaluation"]["topKmax"])]

    p = subprocess.Popen(args, cwd="../../Java")

    p.wait()

if __name__ == '__main__':

    executeFrameworkPipeline()