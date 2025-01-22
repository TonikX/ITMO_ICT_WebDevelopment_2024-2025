using System.Net;
using System.Net.Sockets;
using System.Text;

namespace ConsoleApp1.task_1;

public class Server
{
    private const int Port = 8080;
    
    public static void Main()
    {
        UdpClient server = new UdpClient(Port);
        IPEndPoint remoteIp = new IPEndPoint(IPAddress.Any, Port);

        Console.WriteLine("Сервер ожидает сообщения...");

        while (true)
        {
            byte[] data = server.Receive(ref remoteIp);
            string message = Encoding.UTF8.GetString(data);

            Console.WriteLine("Получено сообщение: " + message);

            if (message == "Hello, server")
            {
                string response = "Hello, client";
                byte[] responseData = Encoding.UTF8.GetBytes(response);
                
                server.Send(responseData, responseData.Length, remoteIp);
                Console.WriteLine("Отправлен ответ клиенту: " + response);
            }
        }
    }
}