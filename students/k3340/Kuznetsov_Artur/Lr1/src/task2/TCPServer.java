package task2;

import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;

public class TCPServer {

    // TCP требует установки соединения между клиентом и сервером, после чего можно передавать данные.
    public static void main(String[] args) {
        int serverPort = 8000;

        try (ServerSocket serverSocket = new ServerSocket(serverPort)) {
            System.out.println("Сервер ожидает подключения...");

            while (true) {
                // Ожидание клиента
                try (Socket clientSocket = serverSocket.accept();
                     BufferedReader in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
                     PrintWriter out = new PrintWriter(clientSocket.getOutputStream(), true)) {

                    // Получаем параметры от клиента
                    double a = Double.parseDouble(in.readLine());
                    double b = Double.parseDouble(in.readLine());
                    double h = Double.parseDouble(in.readLine());

                    // Вычисляем площадь трапеции
                    double area = (a + b) * h / 2;

                    // Отправляем результат обратно клиенту
                    out.println(area);

                } catch (IOException e) {
                    throw new RuntimeException(e);
                }
            }
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}
