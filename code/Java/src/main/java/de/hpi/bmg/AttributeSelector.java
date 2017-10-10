package de.hpi.bmg;

import com.opencsv.CSVWriter;
import weka.attributeSelection.*;
import weka.core.converters.CSVLoader;
import weka.core.Instances;

import java.io.*;
import java.util.Properties;

public class Main {

    public static void main(String[] args) {

        Properties prop = new Properties();

        InputStream input = null;

        try {
            input = new FileInputStream("config.properties");

            // load a properties file
            prop.load(input);
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }

        Instances data = loadData(prop.getProperty("inputFile"));

        data.deleteAttributeAt(1);

        data.setClassIndex(0);

        ASEvaluation eval;

        switch (prop.getProperty("attributeSelection")) {
            case "SVM-RFE":

                eval = new SVMAttributeEval();

                ((SVMAttributeEval) eval).setPercentThreshold(10);

                ((SVMAttributeEval) eval).setPercentToEliminatePerIteration(10);

                break;

            case "GainRatio":

                eval = new GainRatioAttributeEval();

                break;

            case "ReliefF":

                eval = new ReliefFAttributeEval();

                break;

            default:

                eval = new InfoGainAttributeEval();

        }

        Ranker ranker = new Ranker();

        AttributeSelection attsel = new AttributeSelection();

        attsel.setEvaluator(eval);
        attsel.setSearch(ranker);

        // perform attribute selection

        try {

            CSVWriter writer = new CSVWriter(new FileWriter(prop.getProperty("attributeRankingOutputFile") + prop.getProperty("attributeSelection") + ".csv"), ',');

            String[] header = "attributeName,score,index".split(",");

            writer.writeNext(header);

            attsel.SelectAttributes(data);
            double[][] rankedAtts = attsel.rankedAttributes();
            for (int i = 0; i < rankedAtts.length; i++) {

                String[] entry = (""+rankedAtts[i][1] + "," + data.attribute((int) rankedAtts[i][0]).name() + "," + rankedAtts[i][0]).split(",");

                writer.writeNext(entry);
            }

            writer.close();

            // m_attributeRanking[i][1] -> value
            // m_attributeRanking[i][0] -> ID
            // System.out.println(attsel.toResultsString());
        } catch (Exception e) {
            e.printStackTrace();
        }

    }

    private static Instances loadData(String sourceFile) {

        CSVLoader loader = new CSVLoader();
        try {
            loader.setSource(new File(sourceFile));
            Instances data = loader.getDataSet();
            return data;
        } catch (IOException e) {
            e.printStackTrace();
            // see https://opensource.apple.com/source/Libc/Libc-320/include/sysexits.h
            System.exit(66);
        }
        return null;
    }
}
