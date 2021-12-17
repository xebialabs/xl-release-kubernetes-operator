package com.xebialabs.deployit.integration.test.support;

import de.schlichtherle.truezip.file.TFile;
import de.schlichtherle.truezip.file.TFileReader;

import java.io.BufferedReader;
import java.io.IOException;
import java.nio.charset.Charset;
import java.util.ArrayList;
import java.util.List;

public class TFiles {

    private TFiles() {}

    public static List<String> readLines(String path, String charset) throws IOException {
        List<String> result = new ArrayList<>();
        String line;
        try (BufferedReader bufferedReader = new BufferedReader(new TFileReader(new TFile(path), Charset.forName(charset)))) {
            do {
                line = bufferedReader.readLine();
                if (line != null) {
                    result.add(line);
                }
            } while (line != null);
        }
        return result;
    }

    public static List<String> readLines(String path) throws IOException {
        return readLines(path, "UTF-8");
    }
}
