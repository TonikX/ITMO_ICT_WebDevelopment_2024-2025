### Задание:
Реализовать двухпользовательский или многопользовательский чат. Для максимального количества баллов реализуйте многопользовательский чат.
### Описание решения:
#### Серверная часть (Server.java и ClientHandler.java):
Серверная часть реализована на основе протокола TCP и использует многопоточность для работы с несколькими клиентами одновременно. Сервер сохраняет список подключенных клиентов и передает каждому из них сообщения от других пользователей.

Алгоритм работы сервера:
1. Сервер запускается на порту 8000 и ожидает подключения клиентов.
2. Для каждого подключившегося клиента создается новый поток с помощью класса `ClientHandler`.
3. Клиентские сообщения пересылаются всем другим пользователям чата.
4. В случае завершения работы клиентом его соединение закрывается, а пользователь удаляется из списка подключенных.

Код сервера:
```java
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
```

Класс для обработки клиентов (ClientHandler.java):
```java
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
```

#### Клиентская часть (Client.java):
Клиент подключается к серверу, отправляет и получает сообщения. В клиенте также используется многопоточность: один поток отвечает за получение сообщений, а другой — за их отправку.

Алгоритм работы клиента:
1. Клиент подключается к серверу по адресу и порту.
2. Пользователь вводит свое имя и присоединяется к чату.
3. Один поток отвечает за отправку сообщений, другой — за их чтение.
4. Пользователь может выйти из чата, введя команду `exit`.

Код клиента:
```java
package task4;

import java.io.*;
import java.net.Socket;
import java.nio.charset.StandardCharsets;

public class Client {

    private Socket socket;
    private BufferedReader in;
    private BufferedWriter out;
    private BufferedReader userInput;
    private String nickname;

    public Client(String host, int serverPort) {
        try {
            socket = new Socket(host, serverPort);
            userInput = new BufferedReader(new InputStreamReader(System.in, StandardCharsets.UTF_8));
            in = new BufferedReader(new InputStreamReader(socket.getInputStream(), StandardCharsets.UTF_8));
            out = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream(), StandardCharsets.UTF_8));

            this.setNickname();
            new ReadMessage().start();
            new WriteMessage().start();
        } catch (IOException e) {
            throw new RuntimeException("Ошибка подключения к серверу", e);
        }
    }

    private void setNickname() throws IOException {
        System.out.print("Введите ваше имя: ");
        nickname = userInput.readLine();
        out.write(nickname + " присоединился к чату.\n");
        out.flush();
    }

    private class ReadMessage extends Thread {
        @Override
        public void run() {
            String message;
            try {
                while ((message = in.readLine()) != null) {
                    System.out.println(message);
                }
            } catch (IOException e) {
                System.out.println("Соединение прервано: " + e.getMessage());
            }
        }
    }

    private class WriteMessage extends Thread {
        @Override
        public void run() {
            try {
                String message;
                while ((message = userInput.readLine()) != null) {
                    if (message.equalsIgnoreCase("exit")) {
                        out.write(nickname + " покинул чат.\n");
                        out.flush();
                        socket.close();
                        break;
                    }
                    out.write("[" + nickname + "]: " + message + "\n");
                    out.flush();
                }
            } catch (IOException e) {
                System.out.println("Ошибка отправки сообщения: " + e.getMessage());
            }
        }
    }

    public static void main(String[] args) {
        String host = "localhost";
        int serverPort = 8000;
        new Client(host, serverPort);
    }
}
```