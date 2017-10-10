package de.hpi.bmg;

import com.opencsv.CSVReader;
import weka.core.Instances;
import weka.filters.Filter;
import weka.filters.unsupervised.attribute.Remove;

import java.io.*;
import java.util.ArrayList;
import java.util.List;

public class AttributeRemover {

    public static Instances removeUnusedAttributes(Instances data, int numberOfAttributesRetained, String attributeRankingOutputFileLocation) {

        CSVReader reader = null;
        List<String[]> lines = null;

        try {
            reader = new CSVReader(new FileReader(attributeRankingOutputFileLocation), ',');

            String[] header = reader.readNext();

            lines = reader.readAll();

        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }

        List<String[]> subItems = new ArrayList<String[]>(lines.subList(0, numberOfAttributesRetained));

        List<String> attributeIndices = new ArrayList<String>();

        attributeIndices.add("1");

        for (String[] item : subItems) {
            attributeIndices.add("" + ((int) Float.parseFloat(item[2]) + 1));
        }

        Remove remove = new Remove();

        remove.setAttributeIndices(String.join(",",attributeIndices));

        remove.setInvertSelection(true);

        Instances newData = null;

        try {
            remove.setInputFormat(data);
            newData = Filter.useFilter(data, remove);
        } catch (Exception e) {
            e.printStackTrace();
        }

        return newData;

    }
}
