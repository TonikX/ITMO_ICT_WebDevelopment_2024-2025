using System.Net;
using System.Net.Sockets;
using System.Text;

namespace ConsoleApp1.task_1;

public class Client
{
    private const int PortServerEndpoint = 8080;
    private const int PortIpEndPoint = 0;
    
    public static void Main()
    {
        UdpClient client = new UdpClient();
        IPEndPoint serverEndPoint = new IPEndPoint(IPAddress.Parse("127.0.0.1"), PortServerEndpoint);
        
        string message = "Hello, server";
        byte[] data = Encoding.UTF8.GetBytes(message);
        
        client.Send(data, data.Length, serverEndPoint);
        Console.WriteLine("Сообщение отправлено серверу: " + message);
        
        IPEndPoint remoteIp = new IPEndPoint(IPAddress.Any, PortIpEndPoint);
        byte[] response = client.Receive(ref remoteIp);
        
        string responseMessage = Encoding.UTF8.GetString(response);
        Console.WriteLine("Ответ от сервера: " + responseMessage);
        
        client.Close();
    }
}