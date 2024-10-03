package task3;

import java.io.*;
import java.net.ServerSocket;

public class HTTPServer {
    public static void main(String[] args) {
        int serverPort = 8000;
        try (var socket = new ServerSocket(serverPort)) {
            System.out.println("Сервер запущен");
            try (
                    var clientSocket = socket.accept();
                    var out = new PrintWriter(clientSocket.getOutputStream(), true);
                    var in = new BufferedReader(new FileReader("students/k3340/Kuznetsov_Artur/Lr1/src/task3/index.html"))
            ) {
                System.out.println("Клиент подключен");

                // Чтение HTML-файла
                StringBuilder contentBuilder = new StringBuilder();
                String str;
                while ((str = in.readLine()) != null) {
                    contentBuilder.append(str);
                }

                String htmlContent = contentBuilder.toString();

                // Отправка HTTP-ответа
                out.println("/HTTP/1.1 200 OK");
                out.println("Content-Type: text/html");
                out.println();
                out.println(htmlContent);
                out.flush();
            }
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}