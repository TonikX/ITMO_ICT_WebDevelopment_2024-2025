package ru.barkhatnat.server;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;
import java.nio.charset.StandardCharsets;

public class HttpServer {
    private static final String HTML_FILE_PATH = "task_3/src/main/java/ru/barkhatnat/server/index.html";

    public static void main(String[] args) {
        final String address = args.length > 0 ? args[0] : "localhost";
        final int port = args.length > 1 ? Integer.parseInt(args[1]) : 1234;
        try (ServerSocket serverSocket = new ServerSocket(port)) {
            System.out.println("Сервер запущен на порту " + port);
            while (true) {
                try (Socket clientSocket = serverSocket.accept()) {
                    System.out.println("Подключился клиент: " + clientSocket.getInetAddress() + ":" + clientSocket.getPort());
                    handleRequest(clientSocket);
                } catch (IOException e) {
                    System.err.println("Error accepting client connection: " + e.getMessage());
                }
            }
        } catch (IOException e) {
            System.err.printf("Ошибка передачи данных (%s:%d): %s", address, port, e.getMessage());
        } catch (Exception exception) {
            System.err.println("Ошибка приложения:");
            exception.printStackTrace(System.err);
        }
    }

    private static void handleRequest(Socket clientSocket) {
        try (BufferedReader in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream(), StandardCharsets.UTF_8));
             PrintWriter out = new PrintWriter(clientSocket.getOutputStream(), true)) {

            String requestLine = in.readLine();
            System.out.println("Запрос: " + requestLine);
            String htmlContent = HtmlReader.readHtmlFile(HTML_FILE_PATH);
            HttpResponseSender.sendOkResponseWithContent(out, htmlContent);

        } catch (IOException e) {
            System.err.println("Ошибка отправки запроса " + e.getMessage());
        }
    }
}
