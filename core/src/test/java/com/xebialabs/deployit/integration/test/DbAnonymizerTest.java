package com.xebialabs.deployit.integration.test;

import org.testng.annotations.Test;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import org.xml.sax.InputSource;
import org.xml.sax.SAXException;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import java.io.File;
import java.io.IOException;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;

public class DbAnonymizerTest {

    private static final String DEFAULT_FILE_NAME = "xl-deploy-repository-dump.xml";

    @Test
    public void shouldGenerateDataDump() {
        File dataFile = new File(DEFAULT_FILE_NAME);
        assertTrue(dataFile.exists());
    }

    @Test
    public void validateGeneratedFile() throws IOException, SAXException, ParserConfigurationException {
        DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
        factory.setValidating(false);
        factory.setNamespaceAware(true);
        DocumentBuilder builder = factory.newDocumentBuilder();
        Document document = builder.parse(new InputSource(DEFAULT_FILE_NAME));
        NodeList nodeList = document.getElementsByTagName("dataset").item(0).getChildNodes();
        for (int index = 0; index < nodeList.getLength(); index++) {
            if (nodeList.item(index).getNodeType() == Node.ELEMENT_NODE) {
                Element element = (Element) nodeList.item(index);
                String databaseName = element.getNodeName();

                if (databaseName.equalsIgnoreCase("XLD_CI_PROPERTIES")) {
                    String propertyName = element.getAttribute("name");
                    if (propertyName.equalsIgnoreCase("directoryPath")) {
                        assertEquals("/Environments/somePath", element.getAttribute("string_value"));
                    }
                    if (propertyName.equalsIgnoreCase("password") ||
                            propertyName.equalsIgnoreCase("suPassword")) {
                        assertEquals("password", element.getAttribute("string_value"));
                    }
                }

                if (databaseName.equalsIgnoreCase("XLD_DICT_ENTRIES")) {
                    assertEquals("placeholder", element.getAttribute("value"));
                }

                if (databaseName.equalsIgnoreCase("XLD_DICT_ENC_ENTRIES")) {
                    assertEquals("enc-placeholder", element.getAttribute("value"));
                }
            }
        }
    }
}
