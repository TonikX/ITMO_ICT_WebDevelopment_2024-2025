package ru.barkhatnat.server;

import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;

public class Server {
    private static final int BUFFER_SIZE = 1024;

    public static void main(String[] args) {
        final String address = args.length > 0 ? args[0] : "localhost";
        final int port = args.length > 1 ? Integer.parseInt(args[1]) : 1234;
        try (DatagramSocket serverSocket = new DatagramSocket(port, InetAddress.getByName(address))) {
            System.out.println("Сервер запущен на порту " + port);
            while (true) {
                byte[] receiveData = new byte[BUFFER_SIZE];
                DatagramPacket receivePacket = new DatagramPacket(receiveData, receiveData.length);

                serverSocket.receive(receivePacket);
                String messageFromClient = new String(receivePacket.getData(), 0, receivePacket.getLength());
                System.out.println("Сервер получил сообщение: " + messageFromClient);
                String response = "Hello, client";
                byte[] sendData = response.getBytes();
                InetAddress clientAddress = receivePacket.getAddress();
                int clientPort = receivePacket.getPort();
                DatagramPacket sendPacket = new DatagramPacket(sendData, sendData.length, clientAddress, clientPort);

                serverSocket.send(sendPacket);
                System.out.println("Сервер отправил сообщение клиенту на " + clientAddress + ":" + clientPort);
            }
        } catch (Exception exception) {
            System.err.println("Ошибка приложения:");
            exception.printStackTrace(System.err);
        }
    }
}