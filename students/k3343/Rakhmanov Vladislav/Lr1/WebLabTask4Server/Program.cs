using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace MultiUserChat
{
    class ChatServer
    {
        private readonly int _port = 8000;
        private readonly List<TcpClient> _clients = new List<TcpClient>();
        private readonly object _lock = new object();

        public async Task Start()
        {
            var listener = new TcpListener(IPAddress.Any, _port);
            listener.Start();

            Console.WriteLine("Chat Server started on port " + _port);

            try
            {
                while (true)
                {
                    var client = await listener.AcceptTcpClientAsync();
                    lock (_lock)
                    {
                        _clients.Add(client);
                    }

                    Task.Run(() => HandleClient(client));
                }
            }
            finally
            {
                listener.Stop();
            }
        }

        private void HandleClient(TcpClient client)
        {
            NetworkStream stream = null;
            try
            {
                stream = client.GetStream();
                byte[] buffer = new byte[1024];
                int bytesRead;

                while ((bytesRead = stream.Read(buffer, 0, buffer.Length)) != 0)
                {
                    string message = Encoding.UTF8.GetString(buffer, 0, bytesRead);
                    Console.WriteLine($"Received from {client.Client.RemoteEndPoint}: {message}");

                    // Рассылаем сообщение всем клиентам
                    BroadcastMessage(message);
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
            }
            finally
            {
                if (stream != null)
                {
                    stream.Close();
                }

                lock (_lock)
                {
                    _clients.Remove(client);
                }

                client.Close();
            }
        }

        private void BroadcastMessage(string message)
        {
            lock (_lock)
            {
                foreach (var client in _clients)
                {
                    try
                    {
                        NetworkStream stream = client.GetStream();
                        byte[] data = Encoding.UTF8.GetBytes(message);
                        stream.Write(data, 0, data.Length);
                    }
                    catch (Exception ex)
                    {
                        Console.WriteLine(ex.Message);
                    }
                }
            }
        }

        static void Main(string[] args)
        {
            var server = new ChatServer();
            server.Start().Wait();
        }
    }
}
