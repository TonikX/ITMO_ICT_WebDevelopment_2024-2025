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
