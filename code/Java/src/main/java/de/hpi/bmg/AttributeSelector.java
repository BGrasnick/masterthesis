package de.hpi.bmg;

import com.opencsv.CSVWriter;
import weka.attributeSelection.*;
import weka.core.Instances;

import java.io.*;
import java.util.logging.Logger;

public class AttributeSelector {

    private final static Logger LOGGER = Logger.getLogger(AttributeSelector.class.getName());

    private String selectionMethod;
    private Instances data;
    private AttributeSelection attributeSelection;

    public AttributeSelector(Instances data, String selectionMethod){

        this.data = data;
        this.selectionMethod = selectionMethod;

    }

    public void selectAttributes() {
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

        this.attributeSelection = new AttributeSelection();

        this.attributeSelection.setEvaluator(eval);
        this.attributeSelection.setSearch(ranker);

        // perform attribute selection

        long begin = System.currentTimeMillis();

        try {
            this.attributeSelection.SelectAttributes(data);
        } catch (Exception e) {
            e.printStackTrace();
        }

        long end = System.currentTimeMillis();

        long dt = end - begin;

        LOGGER.info("" + dt + "," + this.selectionMethod);
    }

    public void saveSelectedAttributes(String saveLocation) {

        try {

            CSVWriter writer = new CSVWriter(new FileWriter(saveLocation + "/" + this.selectionMethod + ".csv"), ',');

            String[] header = {"attributeName","score","index"};

            writer.writeNext(header);

            double[][] rankedAttributes = this.attributeSelection.rankedAttributes();

            for (int i = 0; i < rankedAttributes.length; i++) {

                String attributeName = data.attribute((int) rankedAttributes[i][0]).name();

                String score = "" + rankedAttributes[i][1];

                String index = "" + (int) rankedAttributes[i][0];

                String[] entry = {attributeName, score, index};

                writer.writeNext(entry);
            }

            writer.close();

        } catch (Exception e) {
            e.printStackTrace();
        }

    }
}
