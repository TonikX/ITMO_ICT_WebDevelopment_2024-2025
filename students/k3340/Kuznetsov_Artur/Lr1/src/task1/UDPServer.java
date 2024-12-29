package task1;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;

public class UDPServer {

    // UDP не требует установки соединения. Клиент просто отправляет датаграмму (пакет данных),
    // а сервер принимает её, не устанавливая явного соединения
    public static void main(String[] args) {
        int serverPort = 8000;
        int bufferSize = 1024;
        String responseMessage = "Hello, server!";

        // Сокет для приема данных на порту 8000
        try (DatagramSocket serverSocket = new DatagramSocket(serverPort)) {
            byte[] receiveData = new byte[bufferSize];

            System.out.println("Сервер ожидает сообщений...");

            // Бесконечный цикл для прослушивания сообщений
            while (true) {
                try {
                    // Прием пакета от клиента
                    DatagramPacket receivePacket = new DatagramPacket(receiveData, receiveData.length);
                    serverSocket.receive(receivePacket);

                    // Вывод сообщения клиента
                    String message = new String(receivePacket.getData()).trim();
                    System.out.println("Получено сообщение от клиента: " + message);

                    // Отправка ответа клиенту
                    InetAddress clientAddress = receivePacket.getAddress();
                    int clientPort = receivePacket.getPort();
                    byte[] sendData = responseMessage.getBytes();
                    DatagramPacket sendPacket = new DatagramPacket(sendData, sendData.length, clientAddress, clientPort);
                    serverSocket.send(sendPacket);
                } catch (IOException e) {
                    throw new RuntimeException(e);
                }
            }
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}
