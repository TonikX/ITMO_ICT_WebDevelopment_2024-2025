### Задание 1: 
Реализовать клиентскую и серверную часть приложения. Клиент отправляет серверу сообщение и оно должно отобразиться на стороне сервера. В ответ сервер отправляет клиенту уведомление, которое должно отобразиться у клиента.

Требования:

Обязательно использовать библиотеку socket. Реализовать с помощью протокола UDP.

Листинг кода серверной части:

```c#
using System;
using System.Net;
using System.Net.Sockets;
using System.Text;

namespace web_lab_1;

class Program
{
    static void Main(string[] args)
    {
        const string ip = "127.0.0.1";
        const int port = 8080;

        var udpEndPoint = new IPEndPoint(IPAddress.Parse(ip), port);

        var udpSocket = new Socket(AddressFamily.InterNetwork, SocketType.Dgram, ProtocolType.Udp);
        udpSocket.Bind(udpEndPoint);

        while (true)
        {
            var buffer = new byte[256];
            var size = 0;
            var data = new StringBuilder();
            EndPoint senderEndPoint = new IPEndPoint(IPAddress.Any, 0);

            do
            {
                size = udpSocket.ReceiveFrom(buffer, ref senderEndPoint);
                data.Append(Encoding.UTF8.GetString(buffer));
            }
            while (udpSocket.Available > 0);



            udpSocket.SendTo(Encoding.UTF8.GetBytes("Сообщение получено."), senderEndPoint);

            Console.WriteLine(data);
        }


    }
}
```

Листинг кода клиентской части:

```c#
using System.Net.Sockets;
using System.Net;
using System.Text;

namespace ClientUdp;

public class Program
{
    static void Main(string[] args)
    {
        const string ip = "127.0.0.1";
        const int port = 8081;

        var udpEndPoint = new IPEndPoint(IPAddress.Parse(ip), port);

        var udpSocket = new Socket(AddressFamily.InterNetwork, SocketType.Dgram, ProtocolType.Udp);
        udpSocket.Bind(udpEndPoint);

        while (true)
        {
            Console.WriteLine("Введите сообщение: ");
            var message = Console.ReadLine();

            var serverEndPoint = new IPEndPoint(IPAddress.Parse("127.0.0.1"), 8080);
            udpSocket.SendTo(Encoding.UTF8.GetBytes(message), serverEndPoint);

            var buffer = new byte[256];
            var size = 0;
            var data = new StringBuilder();
            EndPoint senderEndPoint = new IPEndPoint(IPAddress.Any, 0);

            do
            {
                
                size = udpSocket.ReceiveFrom(buffer, ref senderEndPoint);
                data.Append(Encoding.UTF8.GetString(buffer));
            }
            while (udpSocket.Available > 0);


            Console.WriteLine(data);
            Console.ReadLine();
        }
    }

}
```

Объяснение:

Запускаем файл севера, потом клиента; происходит обмен сообщениями. Обмен происходит при помощи протокола UDP.