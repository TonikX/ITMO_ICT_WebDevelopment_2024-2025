### Задание:
Реализовать клиентскую и серверную часть приложения. Клиент запрашивает выполнение математической операции, параметры которой вводятся с клавиатуры. Сервер обрабатывает данные и возвращает результат клиенту.
### Описание решения:

#### Клиентская часть (TCPClient.java):
Клиент реализован с использованием библиотеки `java.net` и протокола TCP. Алгоритм работы:
- Клиент подключается к серверу через TCP-сокет.
- Вводит с клавиатуры значения параметров для вычисления площади трапеции: длины оснований `a`, `b` и высоты `h`.
- Передает параметры на сервер.
- Получает результат от сервера и выводит его на экран.

Код клиента:
```java
package task2;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.util.Scanner;

public class TCPClient {

    public static void main(String[] args) {
        String serverAddress = "localhost";
        int serverPort = 8000;

        try (Socket socket = new Socket(serverAddress, serverPort);
             BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
             PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
             Scanner scanner = new Scanner(System.in)) {

            // Ввод параметров с клавиатуры
            System.out.println("Введите длину первого основания (a): ");
            double a = scanner.nextDouble();
            System.out.println("Введите длину второго основания (b): ");
            double b = scanner.nextDouble();
            System.out.println("Введите высоту (h): ");
            double h = scanner.nextDouble();

            // Отправляем данные на сервер
            out.println(a);
            out.println(b);
            out.println(h);

            // Получаем результат от сервера
            String response = in.readLine();
            System.out.println("Площадь трапеции: " + response);

        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}
```

#### Серверная часть (TCPServer.java):
Сервер обрабатывает запросы от клиента, вычисляет площадь трапеции на основе переданных данных и отправляет результат обратно клиенту. Алгоритм работы:
- Сервер ожидает подключения клиентов через TCP-сокет на порту 8000.
- Получает от клиента параметры `a`, `b` и `h` для расчета площади трапеции.
- Вычисляет площадь трапеции.
- Отправляет результат клиенту.

Код сервера:
```java
package task2;

import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;

public class TCPServer {

    public static void main(String[] args) {
        int serverPort = 8000;

        try (ServerSocket serverSocket = new ServerSocket(serverPort)) {
            System.out.println("Сервер ожидает подключения...");

            while (true) {
                // Ожидание клиента
                try (Socket clientSocket = serverSocket.accept();
                     BufferedReader in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
                     PrintWriter out = new PrintWriter(clientSocket.getOutputStream(), true)) {

                    // Получаем параметры от клиента
                    double a = Double.parseDouble(in.readLine());
                    double b = Double.parseDouble(in.readLine());
                    double h = Double.parseDouble(in.readLine());

                    // Вычисляем площадь трапеции
                    double area = (a + b) * h / 2;

                    // Отправляем результат обратно клиенту
                    out.println(area);

                } catch (IOException e) {
                    throw new RuntimeException(e);
                }
            }
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}
```