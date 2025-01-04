package students.k3341.Kadnikova_Ekaterina.Lr1.task_1;

import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;

public class Client {
    private static final String MESSAGE = "Hello, server";
    private static final int PORT = 8080;
    private static final String HOST = "localhost";

    public static void main(String[] args) {
        try {
            var socket = new DatagramSocket();
            var serverAddress = InetAddress.getByName(HOST);
            var sendBuffer = MESSAGE.getBytes();
            var sendPacket = new DatagramPacket(sendBuffer, sendBuffer.length, serverAddress, PORT);
            socket.send(sendPacket);
            var receiveBuffer = new byte[1024];
            var receivePacket = new DatagramPacket(receiveBuffer, receiveBuffer.length);
            socket.receive(receivePacket);
            var serverResponse = new String(receivePacket.getData(), 0, receivePacket.getLength());
            System.out.println("Message from server: " + serverResponse);
            socket.close();
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
    }
}