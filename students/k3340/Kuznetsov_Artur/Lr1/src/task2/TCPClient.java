package task2;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.util.Scanner;

public class TCPClient {

    // TCP требует установки соединения между клиентом и сервером, после чего можно передавать данные.
    public static void main(String[] args) {
        String serverAddress = "localhost";
        int serverPort = 8000;

        try (Socket socket = new Socket(serverAddress, serverPort);
             BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
             PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
             Scanner scanner = new Scanner(System.in)) {

            // Ввод параметров с клавиатуры
            System.out.println("Введите длину первого основания (a): ");
            double a = scanner.nextDouble();
            System.out.println("Введите длину второго основания (b): ");
            double b = scanner.nextDouble();
            System.out.println("Введите высоту (h): ");
            double h = scanner.nextDouble();

            // Отправляем данные на сервер
            out.println(a);
            out.println(b);
            out.println(h);

            // Получаем результат от сервера
            String response = in.readLine();
            System.out.println("Площадь трапеции: " + response);

        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}
