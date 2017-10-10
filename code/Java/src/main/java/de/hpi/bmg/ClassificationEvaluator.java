package de.hpi.bmg;

import weka.classifiers.Evaluation;
import weka.classifiers.bayes.NaiveBayes;
import weka.classifiers.functions.Logistic;
import weka.classifiers.functions.SMO;
import weka.classifiers.lazy.IBk;
import weka.core.Instances;

import java.util.Random;

public class ClassificationEvaluator {

    private Instances data;

    public ClassificationEvaluator(String inputFile) {
        DataLoader dl = new DataLoader(inputFile);

        data = dl.getData();

        data.deleteAttributeAt(1);

        data.setClassIndex(0);
    }

    public String trainAndEvaluateWithTopKAttributes(int numberOfAttributesRetained, String attributeRankingOutputFileLocation) {

        Instances newData = AttributeRemover.removeUnusedAttributes(data, numberOfAttributesRetained, attributeRankingOutputFileLocation);

        Evaluation eval = null;

        String returnString = "" + numberOfAttributesRetained;

        try {
            eval = new Evaluation(newData);

            SMO smo = new SMO();
            eval.crossValidateModel(smo, newData, 10, new Random(1));
            returnString += "," + eval.pctCorrect();

            Logistic lr = new Logistic();
            eval.crossValidateModel(lr, newData, 10, new Random(1));
            returnString += "," + eval.pctCorrect();

            NaiveBayes nb = new NaiveBayes();
            eval.crossValidateModel(nb, newData, 10, new Random(1));
            returnString += "," + eval.pctCorrect();

            IBk knn = new IBk();
            knn.setKNN(3);
            eval.crossValidateModel(knn, newData, 10, new Random(1));
            returnString += "," + eval.pctCorrect();

            knn.setKNN(5);
            eval.crossValidateModel(knn, newData, 10, new Random(1));
            returnString += "," + eval.pctCorrect();

            //System.out.println(eval.toSummaryString(true));

            System.out.println(returnString);

        } catch (Exception e) {
            e.printStackTrace();
        }
        return returnString;
    }
}
