package students.k3341.Kadnikova_Ekaterina.Lr1.task_4;

import java.io.*;
import java.net.*;
import java.util.Scanner;

public class Client {
    private static final String HOST = "localhost";
    private static final int PORT = 8080;

    private Socket socket;
    private BufferedReader input;
    private PrintWriter output;

    public Client(String host, int port) {
        try {
            this.socket = new Socket(host, port);
            this.input = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            this.output = new PrintWriter(socket.getOutputStream(), true);
        } catch (IOException e) {
            System.err.println(e.getMessage());
        }
    }

    public void start() {
        new Thread(new ReceivedMessagesHandler()).start();
        var scanner = new Scanner(System.in);
        System.out.println("Enter your name:");
        var userName = scanner.nextLine();
        output.println(userName);

        var message = scanner.nextLine();
        while (!message.equalsIgnoreCase("leave")) {
            output.println(message);
            message = scanner.nextLine();
        }
        try {
            socket.close();
            input.close();
            output.close();
        } catch (IOException e) {
            System.err.println(e.getMessage());
        }
    }

    private class ReceivedMessagesHandler implements Runnable {
        @Override
        public void run() {
            try {
                String message;
                while ((message = input.readLine()) != null) {
                    System.out.println(message);
                }
            } catch (IOException e) {
                System.err.println(e.getMessage());
            }
        }
    }

    public static void main(String[] args) {
        var client = new Client(HOST, PORT);
        client.start();
    }
}
