package de.hpi.bmg;

import com.opencsv.CSVWriter;
import weka.attributeSelection.AttributeSelection;
import weka.core.Instances;

import java.io.FileWriter;
import java.io.IOException;

public class RuntimeMeasurer {

    Instances data;
    String runTimeMeasurementOutput;
    String[] attributeSelectionMethods;

    public RuntimeMeasurer(Instances data, String runTimeMeasurementOutput, String[] attributeSelectionMethods) {
        this.data = data;
        this.runTimeMeasurementOutput = runTimeMeasurementOutput;
        this.attributeSelectionMethods = attributeSelectionMethods;
    }

    public void measureRuntimes(int times) {

        try {

            for (String attributeSelectionMethod : attributeSelectionMethods) {

                CSVWriter writer = new CSVWriter(new FileWriter(runTimeMeasurementOutput + attributeSelectionMethod + ".csv"), ',');

                for (int j = 0; j < 10; j++) {

                    System.out.println(attributeSelectionMethod);

                    String result = Integer.toString(j) + "," + attributeSelectionMethod;

                    AttributeSelector as = new AttributeSelector(data, attributeSelectionMethod);

                    for (int i = 0; i < times; i++) {

                        long begin = System.currentTimeMillis();

                        AttributeSelection attsel = as.selectAttributes();

                        long end = System.currentTimeMillis();

                        long dt = end - begin;

                        System.out.println(dt);

                        result += "," + Long.toString(dt);

                    }

                    writer.writeNext(result.split(","));

                    writer.flush();

                }

            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
