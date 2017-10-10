package de.hpi.bmg;

import com.opencsv.CSVWriter;
import weka.attributeSelection.*;
import weka.core.Instances;

import java.io.*;

public class AttributeSelector {

    private String selectionMethod;
    private Instances data;

    public AttributeSelector(String inputFile, String selectionMethod){

        DataLoader dl = new DataLoader(inputFile);

        data = dl.getData();

        data.deleteAttributeAt(1);

        data.setClassIndex(0);

        this.selectionMethod = selectionMethod;

    }

    public AttributeSelection selectAttributes() {
        ASEvaluation eval;

        switch (this.selectionMethod) {
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
            attsel.SelectAttributes(data);
        } catch (Exception e) {
            e.printStackTrace();
        }

        return attsel;
    }

    public void saveSelectedAttributes(AttributeSelection attsel, String saveLocation) {

        try {

            CSVWriter writer = new CSVWriter(new FileWriter(saveLocation + this.selectionMethod + ".csv"), ',');

            String[] header = {"attributeName","score","index"};

            writer.writeNext(header);

            double[][] rankedAtts = attsel.rankedAttributes();

            for (int i = 0; i < rankedAtts.length; i++) {

                String attributeName = data.attribute((int) rankedAtts[i][0]).name();

                String score = "" + rankedAtts[i][1];

                String index = "" + (int) rankedAtts[i][0];

                String[] entry = {attributeName, score, index};

                writer.writeNext(entry);
            }

            writer.close();

        } catch (Exception e) {
            e.printStackTrace();
        }

    }
}
