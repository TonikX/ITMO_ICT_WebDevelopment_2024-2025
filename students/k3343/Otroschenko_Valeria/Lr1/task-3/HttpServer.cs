using System.Net;
using System.Net.Sockets;
using System.Text;

namespace ConsoleApp1.task_3;

class HttpServer
{
    private const string IpAddress = "127.0.0.1";
    private const int Port = 8080;
    private const int BufferSize = 1024;
    private const int Offset = 0;
    private const string HtmlPath = "/Users/valeriaotrosenko/RiderProjects/ConsoleApp1/ConsoleApp1/task-3/index.html";
    private const string HttpResponseHeader = "HTTP/1.1 200 OK\r\n" +
                                              "Content-Type: text/html; charset=UTF-8\r\n";

    public static void Main()
    {
        IPAddress ip = IPAddress.Parse(IpAddress);
        TcpListener listener = new TcpListener(ip, Port);
        listener.Start();
        Console.WriteLine($"Сервер запущен на {ip}:{Port}. Ожидание подключений...");

        while (true)
        {
            TcpClient client = listener.AcceptTcpClient();
            Console.WriteLine("Клиент подключен.");

            NetworkStream stream = client.GetStream();

            byte[] buffer = new byte[BufferSize];
            int bytesRead = stream.Read(buffer, Offset, buffer.Length);
            string request = Encoding.UTF8.GetString(buffer, Offset, bytesRead);
            Console.WriteLine("Запрос от клиента:\n" + request);

            string htmlContent = File.ReadAllText(HtmlPath);

            string httpResponse = HttpResponseHeader +
                                  $"Content-Length: {htmlContent.Length}\r\n" +
                                  "\r\n" +
                                  htmlContent;

            byte[] responseBytes = Encoding.UTF8.GetBytes(httpResponse);
            stream.Write(responseBytes, Offset, responseBytes.Length);

            stream.Close();
            client.Close();
        }
    }
}