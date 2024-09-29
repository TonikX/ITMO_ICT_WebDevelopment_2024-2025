using System.Net;
using System.Net.Sockets;
using System.Text;

namespace ConsoleApp1.task_4;

class ChatServer
{
    // Список подключенных клиентов
    private static List<TcpClient> clients = new List<TcpClient>();
    private static object lockObject = new object(); // Для синхронизации доступа к списку клиентов

    public static void Main()
    {
        // Устанавливаем IP-адрес и порт
        IPAddress ip = IPAddress.Parse("127.0.0.1");
        int port = 8080;

        // Создаем сервер, прослушивающий подключение
        TcpListener server = new TcpListener(ip, port);
        server.Start();

        Console.WriteLine("Сервер запущен. Ожидание подключений...");

        while (true)
        {
            // Принимаем новое подключение
            TcpClient client = server.AcceptTcpClient();
            Console.WriteLine("Новый клиент подключен.");

            // Добавляем клиента в список
            lock (lockObject)
            {
                clients.Add(client);
            }

            // Запускаем поток для обработки сообщений клиента
            Thread clientThread = new Thread(HandleClient);
            clientThread.Start(client);
        }
    }

    // Обработка клиента
    private static void HandleClient(object clientObject)
    {
        TcpClient client = (TcpClient)clientObject;
        NetworkStream stream = client.GetStream();
        byte[] buffer = new byte[1024];

        try
        {
            while (true)
            {
                // Читаем сообщение от клиента
                int bytesRead = stream.Read(buffer, 0, buffer.Length);
                if (bytesRead == 0) break; // Если клиент отключился

                string message = Encoding.UTF8.GetString(buffer, 0, bytesRead);
                Console.WriteLine("Получено сообщение: " + message);

                // Отправляем сообщение всем клиентам
                BroadcastMessage(message, client);
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine("Ошибка: " + ex.Message);
        }
        finally
        {
            // Удаляем клиента из списка при отключении
            lock (lockObject)
            {
                clients.Remove(client);
            }
            client.Close();
        }
    }

    // Рассылка сообщения всем клиентам, кроме отправителя
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