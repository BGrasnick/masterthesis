import configparser, logging

from preprocessing.discretize import discretize
from preprocessing.filterMissings import filterMissings
from preprocessing.transpose import transpose


def executePipeline():

    config = configparser.ConfigParser()
    config.read('config.ini')

    logging.getLogger().setLevel(logging.INFO)

    logging.info("Starting transposing of data")
    transpose(config["dataLocations"]["sourceDataLocation"], config["dataLocations"]["rawDataLocation"])
    logging.info("Finished transposing of data")

    logging.info("Starting filtering missings in data")
    filterMissings(float(config["missingsFiltering"]["threshold"]), config["dataLocations"]["rawDataLocation"],
                   config["dataLocations"]["missingsFilteredDataLocation"])
    logging.info("Finished filtering missings in data")

    logging.info("Starting discretizing data")
    discretize(config["dataLocations"]["missingsFilteredDataLocation"], config["dataLocations"]["discretizedDataLocation"])
    logging.info("Finished discretizing data")

if __name__ == '__main__':

    executePipeline()