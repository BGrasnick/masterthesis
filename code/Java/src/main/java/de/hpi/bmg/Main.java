package de.hpi.bmg;

import com.opencsv.CSVWriter;
import weka.attributeSelection.AttributeSelection;
import weka.core.Instances;

import java.io.*;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Properties;
import java.util.logging.Logger;

public class Main {

    private final static Logger LOGGER = Logger.getLogger(Main.class.getName());

    public static void main(String[] args) {

        Properties prop = loadProperties("config.properties");

        LOGGER.info(getCurrentTimestamp() + ": Starting loading data from " + prop.getProperty("inputFile"));

        DataLoader dl = new DataLoader(prop.getProperty("inputFile"));

        Instances data = dl.getData();

        LOGGER.info(getCurrentTimestamp() + ": Finished loading data from " + prop.getProperty("inputFile"));

        data.deleteAttributeAt(1);

        data.setClassIndex(0);

        String[] attributeSelectionMethods = {"ReliefF", "SVM-RFE", "GainRatio", "InfoGain"};

        LOGGER.info(getCurrentTimestamp() + ": Starting attribute selection with methods: " + String.join(",",attributeSelectionMethods));

        for (String asMethod : attributeSelectionMethods) {
            selectAttributes(data, asMethod, prop.getProperty("attributeRankingOutputFile"));
        }

        LOGGER.info(getCurrentTimestamp() + ": Finished attribute selection with methods: " + String.join(",",attributeSelectionMethods));

        String[] allMethods = {"ReliefF", "SVM-RFE", "GainRatio", "InfoGain", "disgenetTop15", "disgenetTop25"};

        ClassificationEvaluator ce = new ClassificationEvaluator(data);

        LOGGER.info(getCurrentTimestamp() + ": Starting classification evaluation with models SMO, LR, NB, KNN3, KNN5 with k from " + prop.getProperty("topKmin") + " to " + prop.getProperty("topKmax"));

        for (String asMethod : allMethods) {
            classifyAndEvaluate(prop.getProperty("attributeRankingOutputFile") + asMethod + ".csv", prop.getProperty("resultLocation") + asMethod + ".csv", ce,
                    Integer.parseInt(prop.getProperty("topKmin")), Integer.parseInt(prop.getProperty("topKmax")));
        }

        LOGGER.info(getCurrentTimestamp() + ": Finished classification evaluation with models SMO, LR, NB, KNN3, KNN5 with k from " + prop.getProperty("topKmin") + " to " + prop.getProperty("topKmax"));

        //selectAttributes(data, prop.getProperty("attributeSelection"), prop.getProperty("attributeRankingOutputFile"));
        //removeAttributes(data, prop.getProperty("attributeRankingOutputFile") + prop.getProperty("attributeSelection") + ".csv");
        //classifyAndEvaluate(data, prop.getProperty("attributeRankingOutputFile") + prop.getProperty("attributeSelection") + ".csv");
    }

    private static String getCurrentTimestamp() {
        return new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").format( new Date() );
    }

    private static Properties loadProperties(String propertiesLocation) {

        Properties prop = new Properties();

        InputStream input = null;

        try {
            input = new FileInputStream(propertiesLocation);

            // load a properties file
            prop.load(input);
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }

        return prop;
    }

    private static void classifyAndEvaluate(String attributeRankingFileLocation, String resultLocation, ClassificationEvaluator ce, int topKmin, int topKmax) {

        try {
            CSVWriter writer = new CSVWriter(new FileWriter(resultLocation), ',');

            String[] header = {"#ofAttributes","SMO","LR","NB","KNN3","KNN5"};

            writer.writeNext(header);

            for (int k = topKmin; k <= topKmax; k++) {

                LOGGER.info(getCurrentTimestamp() + ": Starting classification evaluation with models SMO, LR, NB, KNN3, KNN5 with k of " + k);

                String result = ce.trainAndEvaluateWithTopKAttributes(k, attributeRankingFileLocation);
                writer.writeNext(result.split(","));
                writer.flush();

                LOGGER.info(getCurrentTimestamp() + ": Finished classification evaluation with models SMO, LR, NB, KNN3, KNN5 with k of " + k);
            }

            writer.close();
        } catch (IOException e) {
            e.printStackTrace();
        }

    }

    private static void removeAttributes(Instances data, String attributeRankingOutputFileLocation) {

        AttributeRemover.removeUnusedAttributes(data, 100, attributeRankingOutputFileLocation);

    }

    private static void selectAttributes(Instances data, String attributeSelectionMethod, String attributeRankingOutputFile) {

        LOGGER.info(getCurrentTimestamp() + ": Starting attribute selection with method " + attributeSelectionMethod);

        AttributeSelector as = new AttributeSelector(data, attributeSelectionMethod);

        AttributeSelection attsel = as.selectAttributes();

        as.saveSelectedAttributes(attsel, attributeRankingOutputFile);

        LOGGER.info(getCurrentTimestamp() + ": Finished attribute selection with method " + attributeSelectionMethod);

    }


}
