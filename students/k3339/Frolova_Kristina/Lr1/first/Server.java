package first;

import data.Constants;

import java.io.*;
import java.net.*;

public class Server {
    public static void main(String[] args) {
        try (var socket = new DatagramSocket(Constants.port)) {
            var packet = new DatagramPacket(new byte[1024], 1024);
            socket.receive(packet);
            var builder = new StringBuilder();
            for (byte b : packet.getData()) {
                if (b == 0) break;
                builder.append((char) b);
            }
            System.out.println(builder);
            var data = "Hello, client!".getBytes();
            var response = new DatagramPacket(data, data.length, packet.getAddress(), packet.getPort());
            socket.send(response);
        } catch (IOException e) {
            System.out.println("Error: " + e.getMessage());
        }
    }
}
