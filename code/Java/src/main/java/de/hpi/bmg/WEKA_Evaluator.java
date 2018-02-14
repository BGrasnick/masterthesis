package de.hpi.bmg;

import com.opencsv.CSVWriter;
import weka.core.Instances;

import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Properties;
import java.util.logging.Logger;

public class WEKA_Evaluator {

    private final static Logger LOGGER = Logger.getLogger(Main.class.getName());

    public static void main(String[] args) {

        Properties prop = Utils.loadProperties("config.properties");

        DataLoader dl = new DataLoader(args[1]);

        Instances data = dl.getData();

        data.deleteAttributeAt(1);

        data.setClassIndex(0);

        List<String> attributeSelectionMethods = new ArrayList<String>();

        for (int i=2; i < args.length; i++) {
            attributeSelectionMethods.add(args[i]);
        }

        ClassificationEvaluator ce = new ClassificationEvaluator(data);

        for (String asMethod : attributeSelectionMethods) {
            classifyAndEvaluate(prop.getProperty("attributeRankingOutputFile") + asMethod + ".csv", prop.getProperty("resultLocation") + asMethod + ".csv", ce,
                    Integer.parseInt(prop.getProperty("topKmin")), Integer.parseInt(prop.getProperty("topKmax")));
        }
    }

    private static void classifyAndEvaluate(String attributeRankingFileLocation, String resultLocation, ClassificationEvaluator ce, int topKmin, int topKmax) {

        try {
            CSVWriter writer = new CSVWriter(new FileWriter(resultLocation), ',');

            String[] header = {"#ofAttributes","SMO","LR","NB","KNN3","KNN5"};

            writer.writeNext(header);

            for (int k = topKmin; k <= topKmax; k++) {

                //LOGGER.info(getCurrentTimestamp() + ": Starting classification evaluation with models SMO, LR, NB, KNN3, KNN5 with k of " + k + " [" + attributeRankingFileLocation + "]");

                String result = ce.trainAndEvaluateWithTopKAttributes(k, attributeRankingFileLocation);
                writer.writeNext(result.split(","));
                writer.flush();

                //LOGGER.info(getCurrentTimestamp() + ": Finished classification evaluation with models SMO, LR, NB, KNN3, KNN5 with k of " + k + " [" + attributeRankingFileLocation + "]");
            }

            writer.close();
        } catch (IOException e) {
            e.printStackTrace();
        }

    }




}
