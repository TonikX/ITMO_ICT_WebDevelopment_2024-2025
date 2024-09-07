package ru.barkhatnat.server;

import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.logging.Logger;

public class HttpServer {

    private static final int SERVER_PORT = 1234;
    private static final Logger LOGGER = Logger.getLogger(HttpServer.class.getName());
    private static final String HTML_FILE_PATH = "task_3/src/main/java/ru/barkhatnat/server/index.html";
    private static final String HTTP_OK = "HTTP/1.1 200 OK";
    private static final String CONTENT_TYPE = "Content-Type: text/html; charset=UTF-8";

    private final ServerSocket serverSocket;

    public HttpServer() throws IOException {
        serverSocket = new ServerSocket(SERVER_PORT);
        LOGGER.info("Server is ready on port " + SERVER_PORT);
    }

    public void start() {
        while (true) {
            try (Socket clientSocket = serverSocket.accept()) {
                LOGGER.info("Client connected: " + clientSocket.getInetAddress() + ":" + clientSocket.getPort());
                handleRequest(clientSocket);
            } catch (IOException e) {
                LOGGER.severe("Error accepting client connection: " + e.getMessage());
            }
        }
    }

    private static void handleRequest(Socket clientSocket) {
        try (BufferedReader in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
             PrintWriter out = new PrintWriter(clientSocket.getOutputStream(), true)) {

            String requestLine = in.readLine();
            LOGGER.info("Request: " + requestLine);
            String htmlContent = readHtmlFile();
            sendHttpResponse(out, htmlContent);

        } catch (IOException e) {
            LOGGER.severe("Error handling client request: " + e.getMessage());
        }
    }

    private static String readHtmlFile() {
        StringBuilder htmlContent = new StringBuilder();
        String line;

        try (BufferedReader reader = new BufferedReader(new FileReader(HTML_FILE_PATH))) {
            while ((line = reader.readLine()) != null) {
                htmlContent.append(line).append("\n");
            }
        } catch (IOException e) {
            LOGGER.severe("Error reading HTML file: " + e.getMessage());
            return "<html><body><h1>404 NOT FOUND</h1></body></html>";
        }
        return htmlContent.toString();
    }

    private static void sendHttpResponse(PrintWriter out, String htmlContent) {
        out.println(HTTP_OK);
        out.println(CONTENT_TYPE);
        out.println("Content-Length: " + htmlContent.length());
        out.println();
        out.print(htmlContent);
        out.flush();
    }

    public static void main(String[] args) {
        try {
            HttpServer httpServer = new HttpServer();
            httpServer.start();
        } catch (IOException e) {
            LOGGER.severe("IOException occurred: " + e.getMessage());
        }
    }
}
