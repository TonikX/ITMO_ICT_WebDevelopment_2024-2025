using System;
using System.IO;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace MultiUserChat
{
    class ChatClient
    {
        private readonly string _serverIp = "127.0.0.1";
        private readonly int _port = 8000;
        private TcpClient _client;
        private StreamReader _reader;
        private StreamWriter _writer;

        public async Task Connect()
        {
            _client = new TcpClient(_serverIp, _port);
            _reader = new StreamReader(_client.GetStream());
            _writer = new StreamWriter(_client.GetStream()) { AutoFlush = true };

            Task.Run(ReadMessages);

            Console.WriteLine("Connected to the chat server.");
            Console.WriteLine("Enter your messages below:");

            while (true)
            {
                string input = Console.ReadLine();
                if (input == "/exit")
                {
                    break;
                }

                SendMessage(input);
            }

            Disconnect();
        }

        private void ReadMessages()
        {
            while (true)
            {
                try
                {
                    string message = _reader.ReadLine();
                    if (message != null)
                    {
                        Console.WriteLine(message);
                    }
                }
                catch (IOException)
                {
                    break;
                }
            }
        }

        private void SendMessage(string message)
        {
            _writer.WriteLine(message);
        }

        private void Disconnect()
        {
            _client.Close();
            Console.WriteLine("Disconnected from the chat server.");
        }

        static void Main(string[] args)
        {
            var client = new ChatClient();
            client.Connect().Wait();
        }
    }
}