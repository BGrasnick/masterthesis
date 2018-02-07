def writeSetToFile(set, location):

    outputFile = open(location, 'w')
    for item in set:
        outputFile.write("%s\n" % item)
