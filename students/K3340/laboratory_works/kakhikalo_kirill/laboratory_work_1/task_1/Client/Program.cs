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
