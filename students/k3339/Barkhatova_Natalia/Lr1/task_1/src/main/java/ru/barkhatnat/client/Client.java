package ru.barkhatnat.client;

import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.util.logging.Logger;

public class Client {
    private static final Logger LOGGER = Logger.getLogger(Client.class.getName());
    private static final int BUFFER_SIZE = 1024;

    public static void main(String[] args) {
        final String address = args.length > 0 ? args[0] : "localhost";
        final int port = args.length > 1 ? Integer.parseInt(args[1]) : 1234;
        try (DatagramSocket clientSocket = new DatagramSocket()) {
            InetAddress serverAddress = InetAddress.getByName(address);
            String message = "Hello, server";
            byte[] sendData = message.getBytes();

            DatagramPacket sendPacket = new DatagramPacket(sendData, sendData.length, serverAddress, port);
            clientSocket.send(sendPacket);
            System.out.println("Клиент отправил сообщение серверу");

            byte[] receiveData = new byte[BUFFER_SIZE];
            DatagramPacket receivePacket = new DatagramPacket(receiveData, receiveData.length);
            clientSocket.receive(receivePacket);

            String messageFromServer = new String(receivePacket.getData(), 0, receivePacket.getLength());
            System.out.println("Клиент получил сообщение: " + messageFromServer);
        } catch (Exception exception) {
            System.err.println("Ошибка приложения:");
            exception.printStackTrace(System.err);
        }
    }
}