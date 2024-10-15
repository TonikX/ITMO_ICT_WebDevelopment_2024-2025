package fifth;

import data.Constants;

import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

public class Server {

    private static final Map<String, Integer> grades = new HashMap<>();

    public static void main(String[] args) throws IOException {
        try (var socket = new ServerSocket(Constants.port)) {
            while (true) {
                var clientSocket = socket.accept();
                new Thread(() -> handleRequest(clientSocket)).start();
            }
        }
    }

    private static void handleRequest(Socket clientSocket) {
        try (
                var in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
                var out = new BufferedWriter(new OutputStreamWriter(clientSocket.getOutputStream()));
        ) {
            String requestLine = in.readLine();
            if (requestLine != null) {
                var parts = requestLine.split(" ");
                System.out.println(Arrays.toString(parts));
                if (parts.length >= 3 && parts[0].equals("GET") && parts[1].equals("/grades")) {
                    handleGetGrades(out);
                } else if (parts.length >= 3 && parts[0].equals("POST") && parts[1].contains("/addGrade")) {
                    handleAddGrade(in, out);
                } else {
                    sendResponse(out, StatusCode.NOT_FOUND, "Not Found");
                }
            }

        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    private static void handleGetGrades(BufferedWriter out) {
        StringBuilder html = new StringBuilder();
        html.append("<!DOCTYPE html><html lang=\"ru\"><head><meta charset=\"UTF-8\"><title>Список оценок</title></head><body>");
        html.append("<h1>Список оценок</h1>");
        html.append("<ul>");
        for (Map.Entry<String, Integer> entry : grades.entrySet()) {
            html.append("<li>").append(entry.getKey()).append(": ").append(entry.getValue()).append("</li>");
        }
        html.append("</ul>");
        html.append("</body></html>");

        sendResponse(out, StatusCode.OK, html.toString());
    }

    private static void handleAddGrade(BufferedReader in, BufferedWriter out) {
        try {
            String headerLine;
            while (!(headerLine = in.readLine()).isEmpty()) {
                System.out.println(headerLine);
            }

            StringBuilder payload = new StringBuilder();
            while (in.ready()) {
                payload.append((char) in.read());
            }

            String[] params = payload.toString().split("&");
            if (params.length == 2) {
                String discipline = params[0].split("=")[1];
                int grade = Integer.parseInt(params[1].split("=")[1]);

                grades.put(discipline, grade);
                sendResponse(out, StatusCode.OK, "Оценка добавлена");
            } else {
                sendResponse(out, StatusCode.BAD_REQUEST, "Неверный формат запроса");
            }
        } catch (NumberFormatException e) {
            sendResponse(out, StatusCode.BAD_REQUEST, "Некорректная оценка");
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    private static void sendResponse(BufferedWriter out, StatusCode statusCode, String message) {
        try {
            out.write("HTTP/1.1 " + statusCode.getCode() + " " + statusCode + "\r\n");
            out.write("Content-Type: text/html\r\n\r\n");
            out.write(message);
            out.flush();
        } catch (IOException e) {
            System.err.println("Ошибка отправки ответа: " + e.getMessage());
        }
    }
}
