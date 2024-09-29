using System.Net.Sockets;
using System.Text;

namespace ConsoleApp1.task_2;

class Client
{
    private const string ServerIp = "127.0.0.1";
    private const int Port = 8080;
    private const int Offset = 0;
    private const int BufferSize = 1024;

    public static void Main()
    {
        TcpClient client = new TcpClient(ServerIp, Port);
        NetworkStream stream = client.GetStream();

        double baseLength = GetValidatedInput("Введите длину основания параллелограмма: ");
        double height = GetValidatedInput("Введите высоту параллелограмма: ");
        
        byte[] requestBytes = Encoding.UTF8.GetBytes($"{baseLength},{height}");
        
        stream.Write(requestBytes, Offset, requestBytes.Length);

        byte[] buffer = new byte[BufferSize];
        int bytesRead = stream.Read(buffer, Offset, buffer.Length);
        string response = Encoding.UTF8.GetString(buffer, Offset, bytesRead);

        Console.WriteLine($"Площадь параллелограмма: {response}");

        stream.Close();
        client.Close();
    }

    private static double GetValidatedInput(string prompt)
    {
        double result;
        
        while(true)
        {
            Console.Write(prompt);
            var input = Console.ReadLine();

            if (string.IsNullOrEmpty(input))
            {
                Console.WriteLine("Ввод не может быть пустым. Пожалуйста, повторите ввод.");
                continue;
            }

            if (!double.TryParse(input, out result))
            {
                Console.WriteLine("Некорректный ввод. Пожалуйста, введите число.");
                continue;
            }

            break;
        }

        return result;
    }
}