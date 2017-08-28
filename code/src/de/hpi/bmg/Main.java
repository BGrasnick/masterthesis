package de.hpi.bmg;

import weka.attributeSelection.AttributeSelection;
import weka.attributeSelection.InfoGainAttributeEval;
import weka.attributeSelection.Ranker;
import weka.attributeSelection.ReliefFAttributeEval;
import weka.core.Utils;
import weka.core.converters.CSVLoader;
import weka.core.Instances;
import weka.filters.unsupervised.attribute.Remove;
import weka.filters.unsupervised.attribute.RemoveByName;

import java.io.File;
import java.io.IOException;

public class Main {

    public static void main(String[] args) {

        Instances data = loadData("../data/discretized_100_random.csv");

        data.deleteAttributeAt(1);

        data.setClassIndex(0);

        ReliefFAttributeEval eval = new ReliefFAttributeEval();

        Ranker ranker = new Ranker();

        AttributeSelection attsel = new AttributeSelection();

        attsel.setEvaluator(eval);
        attsel.setSearch(ranker);
        // perform attribute selection
        try {
            attsel.SelectAttributes(data);
            int[] indices = attsel.selectedAttributes();
            System.out.println(attsel.toResultsString());
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
