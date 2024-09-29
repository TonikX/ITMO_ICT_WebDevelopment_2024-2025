### Задание:
Написать простой веб-сервер для обработки GET и POST HTTP-запросов с помощью библиотеки `socket` в Python.
### Описание решения:
#### Серверная часть (Server.java):
Программа реализует веб-сервер, который обрабатывает HTTP-запросы и выполняет две основные функции:
1. Обработка GET запроса на получение всех оценок по дисциплинам.
2. Обработка POST запроса для добавления новой дисциплины и оценки.

##### Обработка GET-запросов:
- Сервер принимает GET-запросы по пути `/grades` и возвращает HTML-страницу с перечнем дисциплин и соответствующих оценок.
- Если оценок нет, возвращается сообщение "Нет оценок".

##### Обработка POST-запросов:
- Сервер принимает POST-запросы по пути `/addGrade` и добавляет дисциплину и оценку в список.
- POST-запросы передают данные в формате `discipline=название&grade=оценка`.
- Оценка должна находиться в диапазоне от 1 до 5, иначе сервер возвращает ошибку.

Код сервера:
```java
package task5;

import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.HashMap;
import java.util.Map;

public class Server {

    private static final Map<String, Integer> grades = new HashMap<>();
    private static final int MAX_GRADE = 5;
    private static final int MIN_GRADE = 1;

    public static void main(String[] args) throws IOException {
        final int serverPort = 8000;

        try (ServerSocket serverSocket = new ServerSocket(serverPort)) {
            System.out.println("Сервер запущен");

            while (true) {
                Socket clientSocket = serverSocket.accept();
                new Thread(() -> handleRequest(clientSocket)).start();
            }
        }
    }

    private static void handleRequest(Socket clientSocket) {
        try (
                BufferedReader in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
                BufferedWriter out = new BufferedWriter(new OutputStreamWriter(clientSocket.getOutputStream()))
        ) {
            String requestLine = in.readLine();
            if (requestLine != null) {
                String[] parts = requestLine.split(" ");
                if (parts.length >= 3 && parts[0].equals("GET") && parts[1].equals("/grades")) {
                    handleGetGrades(out);
                } else if (parts.length >= 3 && parts[0].equals("POST") && parts[1].equals("/addGrade")) {
                    handleAddGrade(in, out);
                } else {
                    sendResponse(out, StatusCode.NOT_FOUND, "Not Found");
                }
            }
        } catch (IOException e) {
            System.err.println("Ошибка обработки запроса: " + e.getMessage());
        }
    }

    private static void handleGetGrades(BufferedWriter out) throws IOException {
        StringBuilder html = new StringBuilder();
        html.append("<!DOCTYPE html><html lang=\"ru\"><head><meta charset=\"UTF-8\"><title>Оценки</title></head><body>");
        html.append("<h1>Список оценок по дисциплинам</h1>");
        html.append("<ul>");

        if (grades.isEmpty()) {
            html.append("<li>Нет оценок.</li>");
        } else {
            for (Map.Entry<String, Integer> entry : grades.entrySet()) {
                html.append("<li>").append(entry.getKey()).append(": ").append(entry.getValue()).append("</li>");
            }
        }

        html.append("</ul>");
        html.append("</body></html>");

        sendResponse(out, StatusCode.OK, html.toString());
    }

    private static void handleAddGrade(BufferedReader in, BufferedWriter out) {
        try {
            StringBuilder payload = new StringBuilder();
            while (in.ready()) {
                payload.append((char) in.read());
            }

            String[] params = payload.toString().split("&");
            if (params.length == 2) {
                String discipline = params[0].split("=")[1];
                int grade = Integer.parseInt(params[1].split("=")[1]);

                if (grade < MIN_GRADE || grade > MAX_GRADE) {
                    sendResponse(out, StatusCode.BAD_REQUEST, "Оценка должна быть в диапазоне от " + MIN_GRADE + " до " + MAX_GRADE);
                } else {
                    grades.put(discipline, grade);
                    sendResponse(out, StatusCode.OK, "Оценка добавлена успешно");
                }
            } else {
                sendResponse(out, StatusCode.BAD_REQUEST, "Неверный формат данных");
            }
        } catch (NumberFormatException e) {
            sendResponse(out, StatusCode.BAD_REQUEST, "Некорректная оценка");
        } catch (Exception e) {
            sendResponse(out, StatusCode.BAD_REQUEST, "Ошибка при обработке данных: " + e.getMessage());
        }
    }

    private static void sendResponse(BufferedWriter out, StatusCode statusCode, String message) {
        try {
            out.write("HTTP/1.1 " + statusCode.getCode() + " " + statusCode + "\r\n");
            out.write("Content-Type: text/html; charset=UTF-8\r\n\r\n");
            out.write(message);
            out.flush();
        } catch (IOException e) {
            System.err.println("Ошибка отправки ответа: " + e.getMessage());
        }
    }
}
```