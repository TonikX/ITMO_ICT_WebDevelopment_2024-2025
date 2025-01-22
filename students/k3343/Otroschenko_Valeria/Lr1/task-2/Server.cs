using System.Net;
using System.Net.Sockets;
using System.Text;

namespace ConsoleApp1.task_2;

class Server
{
    private const string IpAddress = "127.0.0.1";
    private const int Port = 8080;
    private const int BufferSize = 1024;
    private const int Offset = 0;

    public static void Main()
    {
        IPAddress ip = IPAddress.Parse(IpAddress);
        TcpListener server = new TcpListener(ip, Port);
        server.Start();

        Console.WriteLine("Сервер запущен. Ожидание подключений...");

        while (true)
        {
            TcpClient client = server.AcceptTcpClient();
            Console.WriteLine("Клиент подключен.");

            NetworkStream stream = client.GetStream();

            byte[] buffer = new byte[BufferSize];
            int bytesRead = stream.Read(buffer, Offset, buffer.Length);
            string request = Encoding.UTF8.GetString(buffer, Offset, bytesRead);
            Console.WriteLine($"Запрос {request} прочитан.");

            string[] parts = request.Split(',');
            double baseLength = double.Parse(parts[0]);
            double height = double.Parse(parts[1]);
            Console.WriteLine($"Клиент прислал данные: длина основания = {baseLength}, высота = {height}");

            double area = baseLength * height;
            Console.WriteLine($"Вычислена площадь = {area}");

            string response = area.ToString();
            byte[] responseBytes = Encoding.UTF8.GetBytes(response);
            stream.Write(responseBytes, Offset, responseBytes.Length);

            stream.Close();
            client.Close();
        }
    }
}