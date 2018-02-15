package de.hpi.bmg;

import com.opencsv.CSVWriter;
import weka.core.Instances;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.logging.Logger;

public class WEKA_Evaluator {

    private final static Logger LOGGER = Logger.getLogger(Main.class.getName());

    public static void main(String[] args) {

        DataLoader dl = new DataLoader(args[0]);

        Instances data = dl.getData();

        data.deleteAttributeAt(1);

        data.setClassIndex(0);

        ClassificationEvaluator ce = new ClassificationEvaluator(data);

        File folder = new File(args[1]);
        File[] listOfFiles = folder.listFiles();

        for (File asMethod : listOfFiles) {
            if (asMethod.isFile()) {
                classifyAndEvaluate(asMethod.getAbsolutePath(), new File(args[2], asMethod.getName()).getAbsolutePath(), ce,
                        Integer.parseInt(args[3]), Integer.parseInt(args[4]));
            }
        }
    }

    private static void classifyAndEvaluate(String attributeRankingFileLocation, String resultLocation, ClassificationEvaluator ce, int topKmin, int topKmax) {

        try {
            CSVWriter writer = new CSVWriter(new FileWriter(resultLocation), ',');

            String[] header = {"#ofAttributes","SMO","LR","NB","KNN3","KNN5", "average"};

            writer.writeNext(header);

            for (int k = topKmin; k <= topKmax; k++) {

                LOGGER.info(": Starting classification evaluation with models SMO, LR, NB, KNN3, KNN5 with k of " + k + " [" + attributeRankingFileLocation + "]");

                String result = ce.trainAndEvaluateWithTopKAttributes(k, attributeRankingFileLocation);
                writer.writeNext(result.split(","));
                writer.flush();

                LOGGER.info(": Finished classification evaluation with models SMO, LR, NB, KNN3, KNN5 with k of " + k + " [" + attributeRankingFileLocation + "]");
            }

            writer.close();
        } catch (IOException e) {
            e.printStackTrace();
        }

    }




}
