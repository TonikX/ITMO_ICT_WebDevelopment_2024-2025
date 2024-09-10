package ru.barkhatnat.server;

import java.io.*;
import java.net.InetAddress;
import java.net.ServerSocket;
import java.net.Socket;

public class Server {


    public static void main(String[] args) {
        final String address = args.length > 0 ? args[0] : "localhost";
        final int port = args.length > 1 ? Integer.parseInt(args[1]) : 1234;
        try (ServerSocket serverSocket = new ServerSocket(port, 0, InetAddress.getByName(address));) {
            System.out.println("Сервер запущен на порту " + port);
            while (true) {
                try (Socket clientSocket = serverSocket.accept();
                     BufferedReader serverInput = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
                     BufferedWriter serverOutput = new BufferedWriter(new OutputStreamWriter(clientSocket.getOutputStream()))) {
                    System.out.println("Клиент приесоединился с порта " + port);
                    String data = serverInput.readLine();
                    System.out.println("Получены данные от клиента: " + data);
                    String response = processInput(data);
                    serverOutput.write(response);
                    serverOutput.flush();
                }
            }
        } catch (IOException e) {
            System.err.printf("Ошибка передачи данных (%s:%d): %s", address, port, e.getMessage());
        } catch (Exception exception) {
            System.err.println("Ошибка приложения:");
            exception.printStackTrace(System.err);
        }
    }

    private static String processInput(String data) {
        StringBuilder response = new StringBuilder();
        try {
            String[] arguments = data.split(" ");
            if (arguments.length < 3) {
                return "Недостаточно аргументов. Ожидается 3 аргумента\n";
            }

            float base1 = Float.parseFloat(arguments[0]);
            float base2 = Float.parseFloat(arguments[1]);
            float height = Float.parseFloat(arguments[2]);
            float result = (base1 + base2) * 0.5f * height;
            response.append("Основание 1: ").append(arguments[0]).append("\n")
                    .append("Основание 2: ").append(arguments[1]).append("\n")
                    .append("Высота: ").append(arguments[2]).append("\n")
                    .append("Площадь трапеции: ").append(result).append("\n");
        } catch (NumberFormatException e) {
            return "Ошибка приведения аргумента к числу\n";
        }
        return response.toString();
    }
}
