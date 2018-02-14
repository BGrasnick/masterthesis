import json, subprocess, os
from preprocessing.addDiseaseCodeToData import addDiseaseCodeToData
from disgenet.disgenetPipeline import executeDisgenetPipeline

def executeFrameworkPipeline():

    jsonFile = open("../../config.json")

    jsonConfig = json.load(jsonFile)

    jsonFile.close()

    # PREPROCESSING

    addDiseaseCodeToData(jsonConfig["preprocessing"]["dataFileLocation"], jsonConfig["preprocessing"]["diseaseCodeFileLocation"], jsonConfig["preprocessing"]["outputLocation"])

    # DISGENET FEATURE SELECTION

    executeDisgenetPipeline(jsonConfig["disgenet"], jsonConfig["preprocessing"]["outputLocation"])

    # VARIANCE BASED FEATURE SELECTION

    p = subprocess.Popen(["Rscript", "VarianceBasedFeatureSelection.R", os.path.abspath(jsonConfig["preprocessing"]["outputLocation"]),
                          jsonConfig["VB-FS"]["featureRankingOutputLocation"], jsonConfig["disgenet"]["filtering"]["geneNameSeparator"]], cwd="../../R")
    p.wait()

    # WEKA FEATURE SELECTION

    args = ["java", "-jar", "../Java/target/WEKA_FeatureSelector.jar", os.path.abspath(jsonConfig["preprocessing"]["outputLocation"]),
                          jsonConfig["WEKA-FS"]["featureRankingOutputLocation"]]

    args.extend(jsonConfig["WEKA-FS"]["FS-methods"])

    p = subprocess.Popen(args, cwd="../../Java")
    p.wait()

if __name__ == '__main__':

    executeFrameworkPipeline()