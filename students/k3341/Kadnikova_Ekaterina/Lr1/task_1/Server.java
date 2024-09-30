package students.k3341.Kadnikova_Ekaterina.Lr1.task_1;

import java.net.DatagramPacket;
import java.net.DatagramSocket;

public class Server {
    private static final String MESSAGE = "Hello, client";
    private static final int PORT = 8080;
    public static void main(String[] args) {
        try {
            var socket = new DatagramSocket(PORT);
            var receiveBuffer = new byte[1024];
            var receivePacket = new DatagramPacket(receiveBuffer, receiveBuffer.length);
            socket.receive(receivePacket);
            var clientMessage = new String(receivePacket.getData(), 0, receivePacket.getLength());
            System.out.println("Message from client: " + clientMessage);
            var sendData = MESSAGE.getBytes();
            var sendPacket = new DatagramPacket(sendData, sendData.length, receivePacket.getAddress(), receivePacket.getPort());
            socket.send(sendPacket);
            socket.close();
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
    }
}