package students.k3341.Kadnikova_Ekaterina.Lr1.task_2;

import java.io.*;
import java.net.*;
import java.util.Scanner;

public class Client {
    private static final String HOST = "localhost";
    private static final int PORT = 8080;

    public static void main(String[] args) {
        try (var socket = new Socket(HOST, PORT);
             var input = new BufferedReader(new InputStreamReader(socket.getInputStream()));
             var output = new PrintWriter(socket.getOutputStream(), true);
             var scanner = new Scanner(System.in)) {

            System.out.println("Enter the first side of parallelogram:");
            var a = scanner.nextDouble();
            System.out.println("Enter the second side of parallelogram:");
            var b = scanner.nextDouble();
            System.out.println("Enter a smaller angle between sides (in degrees):");
            var angle = scanner.nextDouble();

            output.println(a);
            output.flush();
            output.println(b);
            output.flush();
            output.println(angle);
            output.flush();

            var response = input.readLine();
            System.out.println(response);

        } catch (IOException e) {
            System.err.println(e.getMessage());
        }
    }
}
