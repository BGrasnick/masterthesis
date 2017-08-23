package de.hpi.bmg;

import weka.core.converters.CSVLoader;
import weka.core.Instances;

import java.io.File;
import java.io.IOException;

public class Main {

    public static void main(String[] args) {

        Instances data = loadData("../data/discretized.csv");
        
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
