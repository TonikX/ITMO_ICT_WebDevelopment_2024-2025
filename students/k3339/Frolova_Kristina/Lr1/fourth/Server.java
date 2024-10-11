package fourth;

import data.Constants;

import java.io.*;
import java.net.ServerSocket;
import java.util.ArrayList;
import java.util.List;

public class Server {

    public static List<ClientHandler> clients = new ArrayList<>();

    public static void main(String[] args) {
        try (var socket = new ServerSocket(Constants.port)) {
            while (true) {
                try {
                    var clientSocket = socket.accept();
                    clients.add(new ClientHandler(clientSocket));
                } catch (IOException e) {
                    break;
                }
            }
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}
