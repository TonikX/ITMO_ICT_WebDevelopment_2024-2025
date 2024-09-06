package ru.barkhatnat.client;

import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.util.logging.Level;
import java.util.logging.Logger;

public class Client {
    private static final Logger LOGGER = Logger.getLogger(Client.class.getName());
    private static final String SERVER_ADDRESS = "localhost";
    private static final int SERVER_PORT = 1234;
    private static final int BUFFER_SIZE = 1024;

    public static void main(String[] args) {
        try (DatagramSocket clientSocket = new DatagramSocket()) {
            InetAddress serverAddress = InetAddress.getByName(SERVER_ADDRESS);
            String message = "Hello, server";
            byte[] sendData = message.getBytes();

            DatagramPacket sendPacket = new DatagramPacket(sendData, sendData.length, serverAddress, SERVER_PORT);
            clientSocket.send(sendPacket);
            LOGGER.info("Client sent message to server");

            byte[] receiveData = new byte[BUFFER_SIZE];
            DatagramPacket receivePacket = new DatagramPacket(receiveData, receiveData.length);
            clientSocket.receive(receivePacket);

            String messageFromServer = new String(receivePacket.getData(), 0, receivePacket.getLength());
            LOGGER.info("Client received: " + messageFromServer);
        } catch (Exception e) {
            LOGGER.log(Level.SEVERE, "Server encountered an error: ", e);
        }
    }
}