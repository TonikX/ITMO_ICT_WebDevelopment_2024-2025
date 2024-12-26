### Задание:
Реализовать клиентскую и серверную часть приложения. Клиент отправляет серверу сообщение «Hello, server», и оно должно отобразиться на стороне сервера. В ответ сервер отправляет клиенту сообщение «Hello, client», которое должно отобразиться у клиента.

### Описание решения:
#### Клиентская часть (UDPClient.java):
Клиент реализован с использованием библиотеки `java.net` и протокола UDP. Алгоритм работы:
- Создается UDP-сокет для отправки и получения данных.
- Клиент отправляет серверу сообщение «Hello, server» на порт 8000.
- Ожидается ответ от сервера.
- Ответ выводится в консоль клиента.

Код клиента:
```java
package task1;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;

public class UDPClient {

    public static void main(String[] args) {
        int serverPort = 8000;
        int bufferSize = 1024;
        String message = "Hello, server!";

        try {
            DatagramSocket clientSocket = new DatagramSocket();

            InetAddress serverAddress = InetAddress.getByName("localhost");
            byte[] sendData = message.getBytes();
            DatagramPacket sendPacket = new DatagramPacket(sendData, sendData.length, serverAddress, serverPort);
            clientSocket.send(sendPacket);

            byte[] receiveData = new byte[bufferSize];
            DatagramPacket receivePacket = new DatagramPacket(receiveData, receiveData.length);
            clientSocket.receive(receivePacket);

            String response = new String(receivePacket.getData()).trim();
            System.out.println("Ответ от сервера: " + response);

            clientSocket.close();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}
```

#### Серверная часть (UDPServer.java):
Сервер ожидает сообщения от клиента на порту 8000 и отвечает ему сообщением «Hello, client». Алгоритм работы:
- Создается UDP-сокет для приема пакетов.
- Сервер постоянно слушает порт 8000.
- При получении сообщения от клиента, оно выводится в консоль сервера.
- В ответ клиенту отправляется сообщение «Hello, client».

Код сервера:
```java
package task1;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;

public class UDPServer {

    public static void main(String[] args) {
        int serverPort = 8000;
        int bufferSize = 1024;
        String responseMessage = "Hello, client!";

        try (DatagramSocket serverSocket = new DatagramSocket(serverPort)) {
            byte[] receiveData = new byte[bufferSize];

            System.out.println("Сервер ожидает сообщений...");

            while (true) {
                DatagramPacket receivePacket = new DatagramPacket(receiveData, receiveData.length);
                serverSocket.receive(receivePacket);

                String message = new String(receivePacket.getData()).trim();
                System.out.println("Получено сообщение от клиента: " + message);

                InetAddress clientAddress = receivePacket.getAddress();
                int clientPort = receivePacket.getPort();
                byte[] sendData = responseMessage.getBytes();
                DatagramPacket sendPacket = new DatagramPacket(sendData, sendData.length, clientAddress, clientPort);
                serverSocket.send(sendPacket);
            }
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}
```