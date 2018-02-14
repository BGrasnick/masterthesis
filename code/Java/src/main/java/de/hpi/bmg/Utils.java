package de.hpi.bmg;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.util.Properties;

public class Utils {

    static Properties loadProperties(String propertiesLocation) {

        Properties prop = new Properties();

        InputStream input = null;

        try {
            input = new FileInputStream(propertiesLocation);

            // load a properties file
            prop.load(input);
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }

        return prop;
    }

}
