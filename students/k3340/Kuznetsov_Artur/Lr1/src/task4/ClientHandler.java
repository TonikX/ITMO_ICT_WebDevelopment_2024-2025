package task4;

import java.io.*;
import java.net.Socket;
import java.nio.charset.StandardCharsets;

public class ClientHandler extends Thread {

    private final Socket socket;
    private BufferedReader in;
    private BufferedWriter out;

    public ClientHandler(Socket socket) throws IOException {
        this.socket = socket;
        in = new BufferedReader(new InputStreamReader(socket.getInputStream(), StandardCharsets.UTF_8));
        out = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream(), StandardCharsets.UTF_8));
        start();
    }

    @Override
    public void run() {
        try {
            String message;
            while ((message = in.readLine()) != null) {
                System.out.println("Новое сообщение: " + message);
                broadcastMessage(message);
            }
        } catch (IOException e) {
            System.out.println("Клиент отключился: " + e.getMessage());
        } finally {
            endConnection();
        }
    }

    private void broadcastMessage(String message) {
        for (ClientHandler client : Server.clients) {
            if (client != this) {
                try {
                    client.out.write(message + "\n");
                    client.out.flush();
                } catch (IOException e) {
                    System.out.println("Ошибка при отправке сообщения: " + e.getMessage());
                }
            }
        }
    }

    private void endConnection() {
        try {
            if (!socket.isClosed()) {
                socket.close();
                in.close();
                out.close();
            }
        } catch (IOException e) {
            System.out.println("Ошибка закрытия соединения: " + e.getMessage());
        }
    }
}
