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

        var a = 0;
        var b = 0;
        Console.WriteLine("Write a and b of equation a^2 + b^2 = c^2 to get c:");
        var aB = Console.ReadLine().Split(' ');
        if (aB.Length != 2 || !int.TryParse(aB[0], out a) || !int.TryParse(aB[1], out b))
        {
            Console.WriteLine("Invalid input, exiting.");
            return;
        }

        var url = $"http://127.0.0.1:22102/math?a={a}&b={b}";

        using var client = new HttpClient();
        try
        {
            var response = await client.GetAsync(url);
            var resultString = await response.Content.ReadAsStringAsync();
            if (float.TryParse(resultString, out float c))
                Console.WriteLine($"The value of c is: {c}");
            else
                Console.WriteLine("Failed to parse the response as a float.");
        }
        catch (Exception ex)
        {
            Console.WriteLine($"An error occurred: {ex.Message}.");
        }
    }
}