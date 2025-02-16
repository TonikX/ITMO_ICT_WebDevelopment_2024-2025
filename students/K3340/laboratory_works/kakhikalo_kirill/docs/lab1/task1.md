# Задание 1

Реализовать клиентскую и серверную часть приложения. Клиент отправляет серверу сообщение «Hello, server»,
и оно должно отобразиться на стороне сервера. В ответ сервер отправляет клиенту сообщение «Hello, client»,
которое должно отобразиться у клиента.

# Требования

- Обязательно использовать библиотеку socket.
- Реализовать с помощью протокола UDP.

# Ход работы

Сделан клиентский и серверный проект на C#, каждый из которых используют сокеты напрямую,
без каких-либо надстроек, чтобы это совпадало с тем, что есть в socket в Python.

Сервер поднимает UDP сокет, слушает от всех кто и что ему отправит и как только получит полноценное
сообщение "Hello, server" - отправляет обратно "Hello, client".
Учтено, что сообщение может прийти не целиком и уйти тоже не целиком.
Дропы пакетов не учитываются, потому что было разрешено так.

# Листинг кода

#### Сервер

```csharp
using System.Collections.Concurrent;
using System.Net;
using System.Net.Sockets;
using System.Text;

namespace Server;

class Program
{
    static async Task Main(string[] args)
    {
        var listenPort = 22102;
        var socket = new Socket(AddressFamily.InterNetwork, SocketType.Dgram, ProtocolType.Udp);
        socket.Bind(new IPEndPoint(IPAddress.Any, listenPort));

        // https://stackoverflow.com/questions/38191968/c-sharp-udp-an-existing-connection-was-forcibly-closed-by-the-remote-host
        const int SIO_UDP_CONNRESET = -1744830452;
        socket.IOControl((IOControlCode)SIO_UDP_CONNRESET, new byte[] { 0, 0, 0, 0 }, null);
        socket.SetSocketOption(SocketOptionLevel.IP, SocketOptionName.PacketInformation, true);

        EndPoint client = new IPEndPoint(IPAddress.Any, listenPort);

        var clients = new ConcurrentDictionary<EndPoint, Connection>();
        var buffer = new byte[1024];
        while (true)
        {
            var received = await socket.ReceiveFromAsync(buffer, client);
            if (!clients.TryGetValue(received.RemoteEndPoint, out var connection))
            {
                connection = new Connection(received.RemoteEndPoint);
                clients.TryAdd(received.RemoteEndPoint, connection);
            }

            var isTargetKeysFound = Receive(connection, buffer.AsSpan(0, received.ReceivedBytes));
            if (!isTargetKeysFound)
                continue;

            Console.WriteLine($"Received: {connection.ReceivedData} from {connection.Client}");
            var dataToSend = Encoding.UTF8.GetBytes("Hello, client");
            connection.SendingData = dataToSend;
            connection.SentBytes = 0;
            await Send(socket, connection);
        }
    }

    private static async Task Send(Socket socket, Connection connection)
    {
        var bufferToSend = connection.SendingData.AsMemory(connection.SentBytes,
            connection.SendingData.Length - connection.SentBytes);
        connection.SentBytes += await socket.SendToAsync(bufferToSend, connection.Client);
    }

    private static bool Receive(Connection connection, ReadOnlySpan<byte> receivedBytes)
    {
        connection.ReceivedData.Append(Encoding.UTF8.GetString(receivedBytes));

        const string target = "Hello, server";
        if (connection.ReceivedData.Length < target.Length)
            return false;

        var receivedString = connection.ReceivedData.ToString();
        return receivedString.Contains(target);
    }

    private class Connection
    {
        public readonly EndPoint Client;
        public readonly StringBuilder ReceivedData = new();
        public int SentBytes;
        public byte[]? SendingData;

        public Connection(EndPoint client)
        {
            Client = client;
        }
    }
}
```

#### Клиент

```csharp
using System.Net;
using System.Net.Sockets;
using System.Text;

namespace Client;

class Program
{
    public static async Task Main(string[] args)
    {
        var targetPort = 22102;
        var targetAddress = IPAddress.Parse("127.0.0.1");
        var socket = new Socket(AddressFamily.InterNetwork, SocketType.Dgram, ProtocolType.Udp);
        var targetEndPoint = new IPEndPoint(targetAddress, targetPort);
        
        var dataToSend = Encoding.UTF8.GetBytes("Hello, server");
        var sentBytes = 0;
        var receivedBytes = new byte[1024];
        var receivedBytesCount = 0;

        while (true)
        {
            try
            {
                // Пока нет никакого ответа от сервера шлём сообщения снова
                if (receivedBytesCount == 0)
                {
                    sentBytes += await socket.SendToAsync(dataToSend.AsMemory(sentBytes, dataToSend.Length - sentBytes), targetEndPoint);
                    if (sentBytes == dataToSend.Length)
                        sentBytes = 0;
                }

                try
                {
                    var newlyReceived = await socket.ReceiveAsync(receivedBytes);
                    Console.WriteLine("Received from server:");
                    Console.Write(Encoding.UTF8.GetString(receivedBytes, receivedBytesCount, newlyReceived));
                    receivedBytesCount += newlyReceived;
                }
                catch (SocketException e)
                {
                    if (e.SocketErrorCode == SocketError.TimedOut)
                    {
                        Console.WriteLine("Server is not responding, trying to send message again.");
                    }
                    else
                    {
                        Console.WriteLine(e);
                    }
                }
            }
            catch (Exception e)
            {
                Console.WriteLine(e);
            }
        }
    }
}
```