package students.k3341.Kadnikova_Ekaterina.Lr1.task_3;

import java.io.*;
import java.net.*;

public class Server {
    private static final int PORT = 8080;
    private static final String HTML_FILE_PATH = "students/k3341/Kadnikova_Ekaterina/Lr1/task_3/index.html";

    public static void main(String[] args) {
        try (var socket = new ServerSocket(PORT)) {
            System.out.println("Server is running");

            while (true) {
                try (var clientSocket = socket.accept();
                     var input = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
                     var output = clientSocket.getOutputStream()) {
                    System.out.println("Client is connected");

                    var request = new StringBuilder();
                    String line;
                    while ((line = input.readLine()) != null && !line.isEmpty()) {
                        request.append(line).append("\n");
                    }

                    var htmlContent = loadHtmlFile(HTML_FILE_PATH);
                    var httpResponse = "HTTP/1.1 200 OK\r\n" + "Content-Type: text/html\r\n" + "Content-Length: " + htmlContent.length() + "\r\n" + "\r\n" + htmlContent;

                    output.write(httpResponse.getBytes());
                    output.flush();
                } catch (IOException e) {
                    System.err.println(e.getMessage());
                }
            }
        } catch (IOException e) {
            System.err.println(e.getMessage());
        }
    }

    private static String loadHtmlFile(String filePath) {
        var content = new StringBuilder();

        try (var reader = new BufferedReader(new FileReader(filePath))) {
            String line;
            while ((line = reader.readLine()) != null) {
                content.append(line).append("\n");
            }
        } catch (IOException e) {
            System.err.println(e.getMessage());
        }

        return content.toString();
    }
}
