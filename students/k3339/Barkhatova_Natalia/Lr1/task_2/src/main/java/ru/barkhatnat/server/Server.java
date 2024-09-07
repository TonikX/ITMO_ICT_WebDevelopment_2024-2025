package ru.barkhatnat.server;

import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.logging.Logger;

public class Server {
    private static final int SERVER_PORT = 1234;
    private static final Logger LOGGER = Logger.getLogger(Server.class.getName());
    private final ServerSocket serverSocket;

    public Server() throws IOException {
        serverSocket = new ServerSocket(SERVER_PORT);
        LOGGER.info("Server is ready on port " + SERVER_PORT);
    }

    public void start() {
        while (true) {
            try (Socket clientSocket = serverSocket.accept();
                 BufferedReader serverInput = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
                 BufferedWriter serverOutput = new BufferedWriter(new OutputStreamWriter(clientSocket.getOutputStream()))) {
                LOGGER.info("Client connected on port" + SERVER_PORT);
                String data = serverInput.readLine();
                LOGGER.info("Received data from client: " + data);
                String response = processInput(data);
                serverOutput.write(response);
                serverOutput.flush();
            } catch (IOException e) {
                LOGGER.severe("IOException occurred while handling client: " + e.getMessage());
            }
        }
    }

    private String processInput(String data) {
        StringBuilder response = new StringBuilder();
        try {
            String[] arguments = data.split(" ");
            if (arguments.length < 3) {
                return "Not enough arguments. Expected 3 arguments\n";
            }

            float base1 = Float.parseFloat(arguments[0]);
            float base2 = Float.parseFloat(arguments[1]);
            float height = Float.parseFloat(arguments[2]);
            float result = (base1 + base2) * 0.5f * height;
            response.append("Base 1: ").append(arguments[0]).append("\n")
                    .append("Base 2: ").append(arguments[1]).append("\n")
                    .append("Height: ").append(arguments[2]).append("\n")
                    .append("Trapezoid area: ").append(result).append("\n");
        } catch (NumberFormatException e) {
            return "Error parsing argument to number\n";
        }
        return response.toString();
    }

    public static void main(String[] args) {
        try {
            Server server = new Server();
            server.start();
        } catch (IOException e) {
            LOGGER.severe("IOException occurred: " + e.getMessage());
        }
    }
}
