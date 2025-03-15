package task1;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;

public class UDPClient {

    // UDP не требует установки соединения. Клиент просто отправляет датаграмму (пакет данных),
    // а сервер принимает её, не устанавливая явного соединения
    public static void main(String[] args) {
        int serverPort = 8000;
        int bufferSize = 1024;
        String message = "Hello, server!";

        try {
            // Сокет для отправки и получения данных
            DatagramSocket clientSocket = new DatagramSocket();

            // Отправка сообщения серверу
            InetAddress serverAddress = InetAddress.getByName("localhost");
            byte[] sendData = message.getBytes();
            DatagramPacket sendPacket = new DatagramPacket(sendData, sendData.length, serverAddress, serverPort);
            clientSocket.send(sendPacket);

            // Прием ответа от сервера
            byte[] receiveData = new byte[bufferSize];
            DatagramPacket receivePacket = new DatagramPacket(receiveData, receiveData.length);
            clientSocket.receive(receivePacket);

            // Вывод ответа сервера
            String response = new String(receivePacket.getData()).trim();
            System.out.println("Ответ от сервера: " + response);

            clientSocket.close();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}
