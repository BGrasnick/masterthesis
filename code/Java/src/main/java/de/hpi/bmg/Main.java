package de.hpi.bmg;

import com.opencsv.CSVWriter;
import weka.attributeSelection.AttributeSelection;
import weka.core.Instances;

import java.io.*;
import java.util.Properties;

public class Main {

    public static void main(String[] args) {

        Properties prop = loadProperties("config.properties");

        DataLoader dl = new DataLoader(prop.getProperty("inputFile"));

        Instances data = dl.getData();

        data.deleteAttributeAt(1);

        data.setClassIndex(0);

        /*
        String[] attributeSelectionMethods = {"SVM-RFE", "GainRatio", "InfoGain"};

        for (String asMethod : attributeSelectionMethods) {
            selectAttributes(data, asMethod, prop.getProperty("attributeRankingOutputFile"));
        }
        */

        String[] allMethods = {"SVM-RFE", "GainRatio", "InfoGain", "disgenetTop15", "disgenetTop25"};

        ClassificationEvaluator ce = new ClassificationEvaluator(data);

        for (String asMethod : allMethods) {
            classifyAndEvaluate(prop.getProperty("attributeRankingOutputFile") + asMethod + ".csv", ce);
        }

        //selectAttributes(data, prop.getProperty("attributeSelection"), prop.getProperty("attributeRankingOutputFile"));
        //removeAttributes(data, prop.getProperty("attributeRankingOutputFile") + prop.getProperty("attributeSelection") + ".csv");
        //classifyAndEvaluate(data, prop.getProperty("attributeRankingOutputFile") + prop.getProperty("attributeSelection") + ".csv");
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

    private static void classifyAndEvaluate(String attributeRankingFileLocation, ClassificationEvaluator ce) {

        try {
            CSVWriter writer = new CSVWriter(new FileWriter(attributeRankingFileLocation + "_results" + ".csv"), ',');

            String[] header = {"#ofAttributes","SMO","LR","NB","KNN3","KNN5"};

            writer.writeNext(header);

            for (int k = 2; k <= 30; k++) {
                String result = ce.trainAndEvaluateWithTopKAttributes(k, attributeRankingFileLocation);
                System.out.println(result);
                writer.writeNext(result.split(","));
                writer.flush();
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

        AttributeSelector as = new AttributeSelector(data, attributeSelectionMethod);

        AttributeSelection attsel = as.selectAttributes();

        as.saveSelectedAttributes(attsel, attributeRankingOutputFile);

    }


}
