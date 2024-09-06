package ru.barkhatnat.server;

import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.util.logging.Level;
import java.util.logging.Logger;

public class Server {
    private static final int SERVER_PORT = 1234;
    private static final int BUFFER_SIZE = 1024;
    private static final Logger LOGGER = Logger.getLogger(Server.class.getName());

    public static void main(String[] args) {
        try (DatagramSocket serverSocket = new DatagramSocket(SERVER_PORT)) {
            LOGGER.info("Server is ready on port " + SERVER_PORT);

            while (true) {
                byte[] receiveData = new byte[BUFFER_SIZE];
                DatagramPacket receivePacket = new DatagramPacket(receiveData, receiveData.length);

                serverSocket.receive(receivePacket);
                String messageFromClient = new String(receivePacket.getData(), 0, receivePacket.getLength());
                LOGGER.info("Server received: " + messageFromClient);

                String response = "Hello, client";
                byte[] sendData = response.getBytes();
                InetAddress clientAddress = receivePacket.getAddress();
                int clientPort = receivePacket.getPort();
                DatagramPacket sendPacket = new DatagramPacket(sendData, sendData.length, clientAddress, clientPort);

                serverSocket.send(sendPacket);
                LOGGER.info("Server sent message to client at " + clientAddress + ":" + clientPort);
            }
        } catch (Exception e) {
            LOGGER.log(Level.SEVERE, "Server encountered an error: ", e);
        }
    }
}