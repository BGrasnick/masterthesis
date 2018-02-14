from kegg.utils import writeSetToFile

def combineIdLists(firstListLocation, secondListLocation, combinedListLocation):

    firstIdList = [line.rstrip() for line in open(firstListLocation)]
    secondIdList = [line.rstrip() for line in open(secondListLocation)]

    combined = set(firstIdList).union(set(secondIdList))

    writeSetToFile(combined, combinedListLocation)