pathwayFile = open('ensemblIdListWithGeneralPathways.txt', 'r')
pathwayIdList = pathwayFile.readlines()

diseaseFile = open('ensemblIdListDiseases.txt', 'r')
diseaseIdList = diseaseFile.readlines()

combined = set(pathwayIdList).union(set(diseaseIdList))

outputFile = open('combinedIdsWithGeneralPathways.txt', 'w')
for item in combined:
    outputFile.write("%s" % item)