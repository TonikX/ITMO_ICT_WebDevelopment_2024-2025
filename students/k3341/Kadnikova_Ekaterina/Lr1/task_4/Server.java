package students.k3341.Kadnikova_Ekaterina.Lr1.task_4;

import java.io.*;
import java.net.*;
import java.util.*;
import java.util.concurrent.*;

public class Server {
    private static final int PORT = 8080;
    private static final List<ClientSession> clients = new ArrayList<>();

    public static void main(String[] args) {
        System.out.println("Server is running");

        try (var serverSocket = new ServerSocket(PORT)) {
            while (true) {
                var clientSocket = serverSocket.accept();
                var client = new ClientSession(clientSocket);
                clients.add(client);
                Executors.newSingleThreadExecutor().execute(client);
            }
        } catch (IOException e) {
            System.err.println(e.getMessage());
        }
    }

    private static class ClientSession implements Runnable {
        private final Socket socket;
        private PrintWriter output;
        private BufferedReader input;
        private String username;

        public ClientSession(Socket socket) {
            this.socket = socket;
        }

        @Override
        public void run() {
            try {
                input = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                output = new PrintWriter(socket.getOutputStream(), true);
                username = input.readLine();
                sendToAllClients(username + " joined");
                String message;
                while ((message = input.readLine()) != null) {
                    if (message.equalsIgnoreCase("leave")) {
                        break;
                    }
                    sendToAllClients(username + ": " + message);
                }
                leaveChat();
            } catch (IOException e) {
                System.err.println(e.getMessage());
                leaveChat();
            }
        }

        private void sendToAllClients(String message) {
            for (ClientSession clientHandler : clients) {
                clientHandler.output.println(message);
            }
        }

        private void leaveChat(){
            try {
                clients.remove(this);
                sendToAllClients(username + " left");
                socket.close();
                input.close();
                output.close();
            } catch (IOException e) {
                System.err.println(e.getMessage());
            }
        }
    }
}
