package first;

import data.Constants;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;

public class Client {
    public static void main(String[] args) {
        try (var socket = new DatagramSocket()) {
            var data = "Hello, server".getBytes();
            var address = InetAddress.getByName(Constants.host);
            var packet = new DatagramPacket(data, data.length, address, Constants.port);
            socket.send(packet);
            socket.receive(packet);
            System.out.println(new String(packet.getData()));
        } catch (IOException e) {
            System.out.println("Error: " + e.getMessage());
        }
    }
}
