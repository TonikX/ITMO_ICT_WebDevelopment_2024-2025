package ru.barkhatnat.server;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;

public class HtmlReader {
    private static final String NOT_FOUND_HTML = "<html><body><h1>404 NOT FOUND</h1></body></html>";
    private static final String SERVER_ERROR = "<html><body><h1>500 Internal Server Error</h1></body></html>";

    public static String readHtmlFile(String filePath) {
        StringBuilder htmlContent = new StringBuilder();
        String line;
        File file = new File(filePath);
        if (!file.exists()) {
            return NOT_FOUND_HTML;
        }
        try (BufferedReader reader = new BufferedReader(new FileReader(file))) {
            while ((line = reader.readLine()) != null) {
                htmlContent.append(line).append("\n");
            }
        } catch (IOException e) {
            return SERVER_ERROR;
        }
        return htmlContent.toString();
    }

}
