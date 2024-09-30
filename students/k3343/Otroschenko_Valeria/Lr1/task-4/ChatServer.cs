using System.Net;
using System.Net.Sockets;
using System.Text;

namespace ConsoleApp1.task_4;

class ChatServer
{
    private static List<TcpClient> clients = new List<TcpClient>();
    private static object lockObject = new object();
    
    private const string IpAddress = "127.0.0.1";
    private const int Port = 8080;
    private const int BufferSize = 1024;

    public static void Main()
    {
        IPAddress ip = IPAddress.Parse(IpAddress);
        TcpListener server = new TcpListener(ip, Port);
        server.Start();

        Console.WriteLine($"Сервер запущен на {IpAddress}:{Port}. Ожидание подключений...");

        while (true)
        {
            TcpClient client = server.AcceptTcpClient();
            Console.WriteLine("Новый клиент подключен.");

            lock (lockObject)
            {
                clients.Add(client);
            }

            Thread clientThread = new Thread(HandleClient);
            clientThread.Start(client);
        }
    }

    private static void HandleClient(object clientObject)
    {
        TcpClient client = (TcpClient)clientObject;
        NetworkStream stream = client.GetStream();
        byte[] buffer = new byte[BufferSize];

        try
        {
            while (true)
            {
                int bytesRead = stream.Read(buffer, 0, buffer.Length);
                if (bytesRead == 0) break;

                string message = Encoding.UTF8.GetString(buffer, 0, bytesRead);
                Console.WriteLine("Получено сообщение: " + message);

                BroadcastMessage(message, client);
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine("Ошибка: " + ex.Message);
        }
        finally
        {
            lock (lockObject)
            {
                clients.Remove(client);
            }
            client.Close();
        }
    }

    private static void BroadcastMessage(string message, TcpClient senderClient)
    {
        lock (lockObject)
        {
            foreach (var client in clients)
            {
                if (client != senderClient)
                {
                    NetworkStream stream = client.GetStream();
                    byte[] messageBytes = Encoding.UTF8.GetBytes(message);
                    stream.Write(messageBytes, 0, messageBytes.Length);
                }
            }
        }
    }
}