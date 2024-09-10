package ru.barkhatnat.client;

import java.io.*;
import java.net.Socket;

public class Client {

    public static void main(String[] args) {
        final String address = args.length > 0 ? args[0] : "localhost";
        final int port = args.length > 1 ? Integer.parseInt(args[1]) : 1234;
        try (Socket clientSocket = new Socket(address, port);
             BufferedReader clientInput = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
             BufferedWriter clientOutput = new BufferedWriter(new OutputStreamWriter(clientSocket.getOutputStream()));
             BufferedReader consoleReader = new BufferedReader(new InputStreamReader(System.in))) {

            System.out.println("Подключено к серверу на: " + address + ":" + port);

            System.out.println("Введите два основания и высоту трапеции через пробел");
            String data = consoleReader.readLine();
            clientOutput.write(data + "\n");
            clientOutput.flush();

            System.out.println("Ответ сервера:");
            String serverResponse;
            while ((serverResponse = clientInput.readLine()) != null) {
                System.out.println(serverResponse);
            }
        } catch (IOException e) {
            System.err.printf("Ошибка передачи данных (%s:%d): %s", address, port, e.getMessage());
        }
    }
}
