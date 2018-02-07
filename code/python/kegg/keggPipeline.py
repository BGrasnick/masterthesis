from fetchGenes import fetchGenes
from mapToEnsembl import mapToEnsembl
from combineIdLists import combineIdLists

keggPathwayIdListLocation = "input/pathways.txt"
pathwayGeneIdListLocation = "results/pathwaysExtendedGeneIdList.txt"
pathwayEnsemblIdListLocation = "results/pathwaysExtendedEnsemblIdList.txt"

keggDiseaseIdListLocation = "input/diseases.txt"
diseaseGeneIdListLocation = "results/diseasesGeneIdList.txt"
diseaseEnsemblIdListLocation = "results/diseasesEnsemblIdList.txt"

combinedEnsemblIdListLocation = "results/pathwaysExtendedDiseasesEnsemblIdList.txt"

def executePipeline():
    fetchGenes(keggPathwayIdListLocation, pathwayGeneIdListLocation)
    mapToEnsembl(pathwayGeneIdListLocation, pathwayEnsemblIdListLocation)

    #fetchGenes(keggDiseaseIdListLocation, diseaseGeneIdListLocation)
    #mapToEnsembl(diseaseGeneIdListLocation, diseaseEnsemblIdListLocation)

    combineIdLists(pathwayEnsemblIdListLocation, diseaseEnsemblIdListLocation, combinedEnsemblIdListLocation)


if __name__ == '__main__':
    executePipeline()