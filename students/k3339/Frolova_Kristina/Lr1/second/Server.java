package second;

import data.Constants;

import java.io.BufferedWriter;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.net.ServerSocket;
import java.util.InputMismatchException;
import java.util.Scanner;

public class Server {

    private static final double TRAPEZOID_SQUARE_COEFFICIENT = 0.5;
    private static final String CLIENT_CONNECTED = "Client connected";
    private static final String INPUT_FORMAT_ERROR = "Ошибка! Введён некорректный формат данных. Введите три положительных числовых значения. \n";
    private static final String RESPONSE_TEMPLATE = "Площадь трапеции с введёнными параметрами: %s \n";

    public static void main(String[] args) {
        try (
                var socket = new ServerSocket(Constants.port);
                var clientSocket = socket.accept();
                var in = new Scanner(clientSocket.getInputStream());
                var out = new BufferedWriter(new OutputStreamWriter(clientSocket.getOutputStream()))
        ) {
            System.out.println(CLIENT_CONNECTED);

            while (in.hasNext()) {
                try {
                    var a = in.nextInt();
                    var b = in.nextInt();
                    var height = in.nextInt();
                    out.write(RESPONSE_TEMPLATE.formatted(calculateTrapezoidSquare(a, b, height)));
                    out.flush();
                } catch (InputMismatchException e) {
                    var input = in.nextLine();
                    if (input.equalsIgnoreCase("exit")) {
                        break;
                    }
                    out.write(INPUT_FORMAT_ERROR);
                    out.flush();
                }
            }
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    private static double calculateTrapezoidSquare(int a, int b, int height) {
        return TRAPEZOID_SQUARE_COEFFICIENT * height * (a + b);
    }
}
