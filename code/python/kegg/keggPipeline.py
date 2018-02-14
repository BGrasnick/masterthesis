from kegg.fetchGenes import fetchGenes
from kegg.mapToEnsembl import mapToEnsembl

def executeKEGGPipeline(config, uniprotToEnsemblLocation):
    fetchGenes(config["KEGG_entityIdListLocation"], config["geneIdListLocation"])
    mapToEnsembl(config["geneIdListLocation"], config["ensemblIdListLocation"], config["KEGGtoUniprotLocation"], uniprotToEnsemblLocation)