package second;

import data.Constants;

import java.io.*;
import java.net.Socket;

public class Client {

    private static final String ENTER_TRAPEZIO_PARAMETERS = "Для вывода площади трапеции введите длины оснований и высоты через пробел";

    public static void main(String[] args) {
        try (
                var clientSocket = new Socket(Constants.host, Constants.port);
                var reader = new BufferedReader(new InputStreamReader(System.in));
                var in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
                var out = new BufferedWriter(new OutputStreamWriter(clientSocket.getOutputStream()));
        ) {
            System.out.println(ENTER_TRAPEZIO_PARAMETERS);
            System.out.println(Constants.EXIT_MESSAGE);

            var userInput = reader.readLine();
            out.write(userInput + "\n");
            out.flush();

            String serverResponse;

            while ((serverResponse = in.readLine()) != null) {
                System.out.println(serverResponse);
                userInput = reader.readLine();
                out.write(userInput + "\n");
                out.flush();
            }
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}
