package task4;

import java.io.IOException;
import java.net.ServerSocket;
import java.util.ArrayList;
import java.util.List;

public class Server {

    public static List<ClientHandler> clients = new ArrayList<>();

    public static void main(String[] args) {
        final int serverPort = 8000;

        try (ServerSocket serverSocket = new ServerSocket(serverPort)) {
            System.out.println("Сервер запущен, ожидаем подключения...");
            while (true) {
                try {
                    var clientSocket = serverSocket.accept();
                    ClientHandler clientHandler = new ClientHandler(clientSocket);
                    clients.add(clientHandler);
                    System.out.println("Новый пользователь подключился.");
                } catch (IOException e) {
                    System.err.println("Ошибка подключения клиента: " + e.getMessage());
                }
            }
        } catch (IOException e) {
            throw new RuntimeException("Ошибка при запуске сервера", e);
        }
    }
}