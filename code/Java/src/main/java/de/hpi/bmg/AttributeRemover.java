package de.hpi.bmg;

import com.opencsv.CSVReader;
import weka.filters.unsupervised.attribute.Remove;

import java.io.*;
import java.util.ArrayList;
import java.util.List;
import java.util.Properties;

public class RemoveTest {

    public static void main(String[] args) throws Exception {

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

        Remove remove;



        CSVReader reader = new CSVReader(new FileReader(prop.getProperty("attributeRankingOutputFile") + prop.getProperty("attributeSelection") + ".csv"), ',');

        String[] header = reader.readNext();
        
        List<String[]> lines = reader.readAll();

        List<String[]> subItems = new ArrayList<String[]>(lines.subList(0, 100));

        List<Integer> attributeIndices = new ArrayList<Integer>();

        for (String[] item : subItems) {
            attributeIndices.add((int) Float.parseFloat(item[2]));
        }

        System.out.println(attributeIndices);

        //remove.se
    }


}
