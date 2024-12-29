using System.Net.Sockets;
using System.Text;

namespace ConsoleApp1.task_4;

class Client
{
    private const string ServerIp = "127.0.0.1";
    private const int Port = 8080;
    private const int BufferSize = 1024;
    private const int Offset = 0;

    public static void Main()
    {
        string? userName;
        do
        {
            Console.Write("Введите ваше имя: ");
            userName = Console.ReadLine();
            
            if (string.IsNullOrEmpty(userName))
            {
                Console.WriteLine("Имя не может быть пустым. Пожалуйста, введите ваше имя.");
            }

        } while (string.IsNullOrEmpty(userName));

        TcpClient client = new TcpClient(ServerIp, Port);
        NetworkStream stream = client.GetStream();

        Thread receiveThread = new Thread(() => ReceiveMessages(stream));
        receiveThread.Start();
        
        while (true)
        {
            string? message;
            do
            {
                Console.Write("Введите сообщение: ");
                message = Console.ReadLine();

                if (string.IsNullOrEmpty(message))
                {
                    Console.WriteLine("Сообщение не может быть пустым. Пожалуйста, введите сообщение.");
                }

            } while (string.IsNullOrEmpty(message));

            string formattedMessage = $"{userName}: {message}";
            byte[] messageBytes = Encoding.UTF8.GetBytes(formattedMessage);
            stream.Write(messageBytes, Offset, messageBytes.Length);
        }
    }

    private static void ReceiveMessages(NetworkStream stream)
    {
        byte[] buffer = new byte[BufferSize];
        try
        {
            while (true)
            {
                int bytesRead = stream.Read(buffer, Offset, buffer.Length);
                string message = Encoding.UTF8.GetString(buffer, Offset, bytesRead);
                Console.WriteLine(message);
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine("Ошибка: " + ex.Message);
        }
    }
}