package de.hpi.bmg;

import com.opencsv.CSVWriter;
import weka.attributeSelection.AttributeSelection;
import weka.core.Instances;

import java.io.*;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Properties;
import java.util.logging.Logger;

import static de.hpi.bmg.Utils.loadProperties;

public class Main {

    private final static Logger LOGGER = Logger.getLogger(Main.class.getName());

    public static void main(String[] args) {

        Properties prop = loadProperties("config.properties");

        //LOGGER.info(getCurrentTimestamp() + ": Starting loading data from " + prop.getProperty("inputFile"));

        DataLoader dl = new DataLoader(prop.getProperty("inputFile"));

        Instances data = dl.getData();

        //LOGGER.info(getCurrentTimestamp() + ": Finished loading data from " + prop.getProperty("inputFile"));

        data.deleteAttributeAt(1);

        data.setClassIndex(0);

        String[] attributeSelectionMethods = {"InfoGain", "SVM-RFE", "ReliefF"};

        RuntimeMeasurer rm = new RuntimeMeasurer(data, prop.getProperty("runTimeMeasurementOutput"), attributeSelectionMethods);

        rm.measureRuntimes(10);

        //LOGGER.info(getCurrentTimestamp() + ": Starting attribute selection with methods: " + String.join(",",attributeSelectionMethods));

        /*for (String asMethod : attributeSelectionMethods) {
            selectAttributes(data, asMethod, prop.getProperty("attributeRankingOutputFile"));
        }*/

        //LOGGER.info(getCurrentTimestamp() + ": Finished attribute selection with methods: " + String.join(",",attributeSelectionMethods));


        //String[] allMethods = {"ReliefF", "SVM-RFE", "GainRatio", "InfoGain", "disgenetTop15", "disgenetTop25"};
        String[] allMethods = {"random","random2"};

        ClassificationEvaluator ce = new ClassificationEvaluator(data);

        //LOGGER.info(getCurrentTimestamp() + ": Starting classification evaluation with models SMO, LR, NB, KNN3, KNN5 with k from " + prop.getProperty("topKmin") + " to " + prop.getProperty("topKmax"));
        /*
        for (String asMethod : allMethods) {
            classifyAndEvaluate(prop.getProperty("attributeRankingOutputFile") + asMethod + ".csv", prop.getProperty("resultLocation") + asMethod + ".csv", ce,
                    Integer.parseInt(prop.getProperty("topKmin")), Integer.parseInt(prop.getProperty("topKmax")));
        }
        */
        //LOGGER.info(getCurrentTimestamp() + ": Finished classification evaluation with models SMO, LR, NB, KNN3, KNN5 with k from " + prop.getProperty("topKmin") + " to " + prop.getProperty("topKmax"));

        //selectAttributes(data, prop.getProperty("attributeSelection"), prop.getProperty("attributeRankingOutputFile"));
        //removeAttributes(data, prop.getProperty("attributeRankingOutputFile") + prop.getProperty("attributeSelection") + ".csv");
        //classifyAndEvaluate(data, prop.getProperty("attributeRankingOutputFile") + prop.getProperty("attributeSelection") + ".csv");
    }

    private static String getCurrentTimestamp() {
        return new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").format( new Date() );
    }

    private static void removeAttributes(Instances data, String attributeRankingOutputFileLocation) {

        AttributeRemover.removeUnusedAttributes(data, 100, attributeRankingOutputFileLocation);

    }


}
