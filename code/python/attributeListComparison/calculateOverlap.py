import pandas as pd
from os import listdir
from os.path import isfile, join
import itertools

topK = 50

path = "../../../data/rankedAttributes"

onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]

for first, second in list(itertools.combinations(onlyfiles, 2)):

    firstRanking = pd.read_csv(path + first)
    secondRanking = pd.read_csv(path + second)

    percentageOverlap = len(set(firstRanking["attributeName"].head(topK).tolist())
                            .intersection(secondRanking["attributeName"].head(topK).tolist())) / topK

    print(first + "/" + second + "," + str(percentageOverlap))

