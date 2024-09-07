package ru.barkhatnat.client;

import java.io.*;
import java.net.Socket;
import java.util.logging.Logger;

public class Client {

    private static final int SERVER_PORT = 1234;
    private static final String SERVER_ADDRESS = "localhost";
    private static final Logger LOGGER = Logger.getLogger(Client.class.getName());

    public static void main(String[] args) {
        try (Socket clientSocket = new Socket(SERVER_ADDRESS, SERVER_PORT);
             BufferedReader clientInput = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
             BufferedWriter clientOutput = new BufferedWriter(new OutputStreamWriter(clientSocket.getOutputStream()));
             BufferedReader consoleReader = new BufferedReader(new InputStreamReader(System.in))) {

            LOGGER.info("Connected to server at " + SERVER_ADDRESS + ":" + SERVER_PORT);

            System.out.println("Enter the length of the two bases and the height of the trapezoid separated by a space");
            String data = consoleReader.readLine();
            clientOutput.write(data + "\n");
            clientOutput.flush();

            System.out.println("Server response:\n");
            String serverResponse;
            while ((serverResponse = clientInput.readLine()) != null) {
                System.out.println(serverResponse);
            }
        } catch (IOException ex) {
            LOGGER.severe("IOException occurred: " + ex.getMessage());
        }
    }
}
