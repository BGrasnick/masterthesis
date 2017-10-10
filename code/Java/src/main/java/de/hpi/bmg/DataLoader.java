package de.hpi.bmg;

import weka.core.Instances;
import weka.core.converters.CSVLoader;

import java.io.File;
import java.io.IOException;

public class DataLoader {


    String sourceFile;

    Instances data;

    public DataLoader(String sourceFile) {
        this.sourceFile = sourceFile;
        loadData();
    }

    public Instances getData() {
        return data;
    }

    private void loadData() {

        CSVLoader loader = new CSVLoader();
        try {
            loader.setSource(new File(this.sourceFile));
            this.data = loader.getDataSet();
        } catch (IOException e) {
            e.printStackTrace();
            // see https://opensource.apple.com/source/Libc/Libc-320/include/sysexits.h
            System.exit(66);
        }
    }

}
