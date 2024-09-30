package students.k3341.Kadnikova_Ekaterina.Lr1.task_2;

import java.io.*;
import java.net.*;

public class Server {
    private static final int PORT = 8080;

    public static void main(String[] args) {
        try (var serverSocket = new ServerSocket(PORT)) {
            System.out.println("Server is running");
            try (var clientSocket = serverSocket.accept();
                 var input = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
                 var output = new PrintWriter(clientSocket.getOutputStream(), true)) {
                 System.out.println("Client is connected");
                 try {
                    var aInput = input.readLine();
                    double a = Double.parseDouble(aInput);
                    if (a <= 0) throw new IllegalArgumentException("The length of a side cannot be a non-positive number");

                    var bInput = input.readLine();
                    double b = Double.parseDouble(bInput);
                    if (b <= 0) throw new IllegalArgumentException("The length of a side cannot be a non-positive number");

                    var angleInput = input.readLine();
                    var angle = Double.parseDouble(angleInput);
                    if (angle <= 0 || angle >= 180)
                        throw new IllegalArgumentException("The angle should be between 0 and 180 degrees");

                    var angleInRadians = Math.toRadians(angle);
                    var area = a * b * Math.sin(angleInRadians);

                    output.println("The area of the parallelogram: " + area);
                    System.out.println("The area of the parallelogram: " + area);
                } catch (IllegalArgumentException e) {
                    output.println(e.getMessage());
                    System.err.println(e.getMessage());
                }
            } catch (IOException e) {
                System.err.println(e.getMessage());
            }
        } catch (IOException e) {
            System.err.println(e.getMessage());
        }
    }
}
