package third;

import data.Constants;

import javax.swing.text.html.HTML;
import javax.swing.text.html.HTMLDocument;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintWriter;
import java.net.ServerSocket;

public class Server {
    public static void main(String[] args) {
        try (var socket = new ServerSocket(Constants.port)) {
            System.out.println("Server started");
            try (
                    var clientSocket = socket.accept();
                    var out = new PrintWriter(clientSocket.getOutputStream(), true);
                    var in = new BufferedReader(new FileReader("src/third/index.html"))
            ) {
                System.out.println("Client connected");

                StringBuilder contentBuilder = new StringBuilder();

                String str;
                while ((str = in.readLine()) != null) {
                    contentBuilder.append(str);
                }

                String content = contentBuilder.toString();

                out.println("/HTTP/1.1 200 OK");
                out.println("Content-Type: text/html");
                out.println("\r\n");
                out.println(content);
                out.flush();
            }
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}
