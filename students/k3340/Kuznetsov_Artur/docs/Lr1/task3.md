### Задание:
Реализовать серверную часть приложения. Клиент подключается к серверу, и в ответ получает HTTP-сообщение, содержащее HTML-страницу, которая сервер подгружает из файла `index.html`.

### Описание решения:
#### Серверная часть (HTTPServer.java):
Программа реализует простой HTTP-сервер с использованием сокетов. Сервер принимает подключение от клиента, загружает HTML-страницу из файла `index.html` и отправляет её клиенту в формате HTTP-ответа.

Алгоритм работы:
1. Сервер создается на порту 8000 с помощью класса `ServerSocket`.
2. Сервер ожидает подключения клиента.
3. При подключении клиента, сервер открывает файл `index.html` и считывает его содержимое.
4. HTML-контент отправляется клиенту в формате HTTP-ответа с кодом 200 OK.
5. Соединение с клиентом закрывается.

Код сервера:
```java
package task3;

import java.io.*;
import java.net.ServerSocket;

public class HTTPServer {
    public static void main(String[] args) {
        int serverPort = 8000;
        try (var socket = new ServerSocket(serverPort)) {
            System.out.println("Сервер запущен");
            try (
                    var clientSocket = socket.accept();
                    var out = new PrintWriter(clientSocket.getOutputStream(), true);
                    var in = new BufferedReader(new FileReader("index.html"))
            ) {
                System.out.println("Клиент подключен");

                // Чтение HTML-файла
                StringBuilder contentBuilder = new StringBuilder();
                String str;
                while ((str = in.readLine()) != null) {
                    contentBuilder.append(str);
                }

                String htmlContent = contentBuilder.toString();

                // Отправка HTTP-ответа
                out.println("HTTP/1.1 200 OK");
                out.println("Content-Type: text/html");
                out.println();
                out.println(htmlContent);
                out.flush();
            }
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}
```