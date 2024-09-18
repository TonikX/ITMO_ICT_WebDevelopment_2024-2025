package students.k3341.Kadnikova_Ekaterina.Lr1.task_5;

import java.io.*;
import java.net.*;
import java.util.*;

public class Server {
    private static final int PORT = 8080;
    private static final Map<String, List<Integer>> grades = new HashMap<>();
    private static final String SUBMIT_TEMPLATE_PATH = "students/k3341/Kadnikova_Ekaterina/Lr1/task_5/submitTemplate.html";
    private static final String GRADES_TEMPLATE_PATH = "students/k3341/Kadnikova_Ekaterina/Lr1/task_5/gradesTemplate.html";

    public static void main(String[] args) throws IOException {
        var serverSocket = new ServerSocket(PORT);
        System.out.println("Server is running");

        try {
            while (true) {
                var clientSocket = serverSocket.accept();
                handleClientRequest(clientSocket);
            }
        } catch (IOException e) {
            serverSocket.close();
            throw new RuntimeException(e);
        }
    }

    private static void handleClientRequest(Socket clientSocket) throws IOException {
        var input = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
        var output = clientSocket.getOutputStream();

        var requestLine = input.readLine();
        if (requestLine == null) {
            return;
        }

        var requestParts = requestLine.split(" ");
        var method = requestParts[0];
        var path = requestParts[1];

        if (method.equals("GET") && path.equals("/submit")) {
            sendSubmitPage(output);
        } else if (method.equals("GET") && path.equals("/grades")) {
            sendGradesPage(output);
        } else if (method.equals("POST") && path.equals("/submit")) {
            handlePostRequest(input, output);
        } else {
            sendNotFoundResponse(output);
        }

        input.close();
        output.close();
        clientSocket.close();
    }

    private static void handlePostRequest(BufferedReader input, OutputStream out) throws IOException {
        String line;
        int contentLength = 0;
        while (!(line = input.readLine()).isEmpty()) {
            if (line.startsWith("Content-Length:")) {
                contentLength = Integer.parseInt(line.split(":")[1].trim());
            }
        }

        var body = new char[contentLength];
        input.read(body);
        var requestBody = new String(body);

        var params = requestBody.split("&");
        String discipline = null;
        int grade = 0;
        for (String param : params) {
            String[] keyValue = param.split("=");
            if (keyValue[0].equals("discipline")) {
                discipline = URLDecoder.decode(keyValue[1], "UTF-8");
            } else if (keyValue[0].equals("grade")) {
                grade = Integer.parseInt(keyValue[1]);
            }
        }

        if (discipline != null && grade != 0) {
            grades.computeIfAbsent(discipline, k -> new ArrayList<>()).add(grade);
        }

        var response = "HTTP/1.1 303 See Other\r\n" + "Location: /grades\r\n" + "Content-Length: 0\r\n" + "\r\n";
        out.write(response.getBytes());
    }

    private static void sendSubmitPage(OutputStream out) throws IOException {
        var htmlTemplate = loadHtmlTemplate(SUBMIT_TEMPLATE_PATH);
        var httpResponse = "HTTP/1.1 200 OK\r\n" + "Content-Type: text/html\r\n" + "Content-Length: " + htmlTemplate.length() + "\r\n" + "\r\n" + htmlTemplate;
        out.write(httpResponse.getBytes());
    }

    private static void sendGradesPage(OutputStream out) throws IOException {
        var htmlTemplate = loadHtmlTemplate(GRADES_TEMPLATE_PATH);

        var gradesList = new StringBuilder();
        for (Map.Entry<String, List<Integer>> entry : grades.entrySet()) {
            gradesList.append("<li>").append(entry.getKey()).append(": ").append(entry.getValue()).append("</li>");
        }

        var responseBody = htmlTemplate.replace("<!-- GRADES_LIST -->", gradesList.toString());
        var httpResponse = "HTTP/1.1 200 OK\r\n" + "Content-Type: text/html\r\n" + "Content-Length: " + responseBody.length() + "\r\n" + "\r\n" + responseBody;
        out.write(httpResponse.getBytes());
    }

    private static String loadHtmlTemplate(String filePath) throws IOException {
        var templateContent = new StringBuilder();
        try (var reader = new BufferedReader(new FileReader(filePath))) {
            String line;
            while ((line = reader.readLine()) != null) {
                templateContent.append(line).append("\n");
            }
        }
        return templateContent.toString();
    }

    private static void sendNotFoundResponse(OutputStream out) throws IOException {
        var responseBody = "<html><body><h1>404 Not Found</h1></body></html>";
        var httpResponse = "HTTP/1.1 404 Not Found\r\n" + "Content-Type: text/html\r\n" + "Content-Length: " + responseBody.length() + "\r\n" + "\r\n" + responseBody;
        out.write(httpResponse.getBytes());
    }
}
