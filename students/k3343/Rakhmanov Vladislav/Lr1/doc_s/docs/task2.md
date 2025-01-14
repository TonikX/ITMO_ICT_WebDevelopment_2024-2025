### Задание 2: 
Реализовать клиентскую и серверную часть приложения. Клиент запрашивает выполнение математической операции, параметры которой вводятся с клавиатуры. Сервер обрабатывает данные и возвращает результат клиенту.

Вариант операции: Поиск площади трапеции.

Требования:

Обязательно использовать библиотеку socket. Реализовать с помощью протокола TCP.

Листинг кода серверной части:

```c#
using System;
using System.Net;
using System.Net.Sockets;
using System.Text;

namespace ServerTcp
{
    class Program
    {
        static void Main(string[] args)
        {
            const string ip = "127.0.0.1";
            const int port = 8080;

            var tcpListener = new TcpListener(IPAddress.Parse(ip), port);
            tcpListener.Start();

            Console.WriteLine("Сервер запущен. Ожидание подключений...");

            while (true)
            {
                using (var client = tcpListener.AcceptTcpClient())
                using (var networkStream = client.GetStream())
                {
                    var buffer = new byte[256];
                    var size = networkStream.Read(buffer, 0, buffer.Length);
                    var message = Encoding.UTF8.GetString(buffer, 0, size);

                    var parameters = message.Split(' ');
                    if (parameters.Length == 3 &&
                        double.TryParse(parameters[0], out double a) &&
                        double.TryParse(parameters[1], out double b) &&
                        double.TryParse(parameters[2], out double h))
                    {
                        var area = 0.5 * (a + b) * h;
                        Console.WriteLine($"Получены параметры: a={a}, b={b}, h={h}");
                        Console.WriteLine($"Площадь трапеции: {area}");

                        var response = "Сообщение получено.";
                        var data = Encoding.UTF8.GetBytes(response);
                        networkStream.Write(data, 0, data.Length);
                    }
                    else
                    {
                        var errorResponse = "Неверные параметры. Попробуйте снова.";
                        var errorData = Encoding.UTF8.GetBytes(errorResponse);
                        networkStream.Write(errorData, 0, errorData.Length);
                    }
                }
            }
        }
    }
}
```

Листинг кода клиентской части:

```c#
using System;
using System.Net.Sockets;
using System.Text;

namespace ClientTcp
{
    public class Program
    {
        static void Main(string[] args)
        {
            const string serverIp = "127.0.0.1";
            const int serverPort = 8080;

            while (true)
            {
                Console.WriteLine("Введите основания и высоту трапеции (через пробел): ");
                var message = Console.ReadLine();

                using (var client = new TcpClient(serverIp, serverPort))
                using (var networkStream = client.GetStream())
                {
                    var data = Encoding.UTF8.GetBytes(message);
                    networkStream.Write(data, 0, data.Length);

                    var buffer = new byte[256];
                    var size = networkStream.Read(buffer, 0, buffer.Length);
                    var response = Encoding.UTF8.GetString(buffer, 0, size);

                    Console.WriteLine("Сервер принял сообщение: " + response);
                }
            }
        }
    }
}

```