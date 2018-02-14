package de.hpi.bmg;

import weka.core.Instances;

import java.util.ArrayList;
import java.util.List;

public class WEKA_FeatureSelector {

    public static void main(String[] args) {

        DataLoader dl = new DataLoader(args[0]);

        Instances data = dl.getData();

        data.deleteAttributeAt(1);

        data.setClassIndex(0);

        List<String> attributeSelectionMethods = new ArrayList<String>();

        for (int i=2; i < args.length; i++) {
            attributeSelectionMethods.add(args[i]);
        }

        for (String asMethod : attributeSelectionMethods) {

            AttributeSelector as = new AttributeSelector(data, asMethod);

            as.selectAttributes();

            as.saveSelectedAttributes(args[1]);
        }

    }

}
