package ru.barkhatnat;

import com.sun.net.httpserver.HttpExchange;

import java.io.IOException;
import java.io.OutputStream;
import java.util.HashMap;
import java.util.Map;


public class HttpHandler implements com.sun.net.httpserver.HttpHandler {

    private final Map<String, String> grades;

    public HttpHandler(Map<String, String> grades) {
        this.grades = grades;
    }

    @Override
    public void handle(HttpExchange exchange) throws IOException {
        String method = exchange.getRequestMethod();

        if ("GET".equalsIgnoreCase(method)) {
            handleGetRequest(exchange);
        } else if ("POST".equalsIgnoreCase(method)) {
            handlePostRequest(exchange);
        } else {
            sendResponse(exchange, 405, "Method Not Allowed");
        }
    }

    private void handleGetRequest(HttpExchange exchange) throws IOException {
        StringBuilder response = new StringBuilder("<html><body><h2>Grades</h2><ul>");
        for (Map.Entry<String, String> entry : grades.entrySet()) {
            response.append("<li>").append(entry.getKey()).append(": ").append(entry.getValue()).append("</li>");
        }
        response.append("</ul></body></html>");
        sendResponse(exchange, 200, response.toString());
    }

    private void handlePostRequest(HttpExchange exchange) throws IOException {
        String uri = String.valueOf(exchange.getRequestURI());
        Map<String, String> params = parseQuery(uri);

        String discipline = params.get("discipline");
        String grade = params.get("grade");
        if (discipline != null && grade != null) {
            grades.put(discipline, grade);
            sendResponse(exchange, 200, "Grade saved successfully");
        } else {
            sendResponse(exchange, 400, "Missing discipline or grade");
        }
    }

    private Map<String, String> parseQuery(String uri) {
        Map<String, String> params = new HashMap<>();
        String[] uriParts = uri.split("\\?", 2);
        if (uriParts.length < 2 || uriParts[1].isEmpty()) {
            return params;
        }
        String[] pairs = uriParts[1].split("&");
        for (String pair : pairs) {
            String[] keyValue = pair.split("=", 2);
            if (keyValue.length > 1) {
                params.put(keyValue[0], keyValue[1]);
            } else {
                params.put(keyValue[0], "");
            }
        }
        return params;
    }

    private void sendResponse(HttpExchange exchange, int statusCode, String response) throws IOException {
        exchange.sendResponseHeaders(statusCode, response.length());
        OutputStream os = exchange.getResponseBody();
        os.write(response.getBytes());
        os.close();
    }
}

