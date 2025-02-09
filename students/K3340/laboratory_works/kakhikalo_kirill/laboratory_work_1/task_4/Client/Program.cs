using System.Collections.Concurrent;
using System.Diagnostics.CodeAnalysis;
using System.Net;
using System.Net.Sockets;
using System.Text;

namespace Server;

class Program
{
    static async Task Main(string[] args)
    {
        var listenPort = 22102;
        var socket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
        socket.ReceiveTimeout = 1;
        socket.SendTimeout = 1;
        socket.Connect(IPAddress.Parse("127.0.0.1"), listenPort);

        var connection = new Connection(socket);
        var messages = new ConcurrentQueue<string>();
        var thread = new Thread(() => PollMessages(connection, messages));
        thread.Start();

        var userInputBuffer = new StringBuilder();
        while (true)
        {
            while (messages.TryDequeue(out var result))
            {
                // Всё это нужно чтобы инпут юзера всегда оставался снизу
                var currentCursorPosition = Console.GetCursorPosition();
                Console.SetCursorPosition(0, currentCursorPosition.Top);
                Console.Write(new string(' ', Console.BufferWidth));
                Console.SetCursorPosition(0, currentCursorPosition.Top);

                Console.WriteLine(result);

                if (userInputBuffer.Length > 0)
                    Console.Write(userInputBuffer.ToString());
            }

            if (!Console.KeyAvailable)
                continue;

            var key = Console.ReadKey(true);
            if (key.Key == ConsoleKey.Enter)
            {
                var userInput = userInputBuffer.ToString();
                var dataRaw = Encoding.UTF32.GetBytes(userInput);
                connection.Send(dataRaw);

                userInputBuffer.Clear();
                Console.WriteLine();
            }
            else
            {
                userInputBuffer.Append(key.KeyChar);
                Console.Write(key.KeyChar);
            }
        }
    }

    private static void PollMessages(Connection connection, ConcurrentQueue<string> messages)
    {
        while (true)
        {
            while (connection.PollRead(out var data))
            {
                var message = UTF32Encoding.UTF32.GetString(data);
                messages.Enqueue(message);
            }

            while (connection.PollWrite())
                Thread.Sleep(1);
        }
    }

    private class Connection : IDisposable
    {
        private const int PacketHeaderSize = 2;

        public readonly Socket Client;
        public readonly byte[] ReceiveBuffer = new byte[1024 * 8];
        public readonly byte[] SendBuffer = new byte[1024 * 8];

        private int _sentBytes;
        private int _bytesToSent;
        private int _bytesReceived;
        private int _bytesToReceive;

        public Connection(Socket client)
        {
            Client = client;
        }

        public void Send(Span<byte> data)
        {
            while (PollWrite())
                Thread.Sleep(1);

            var size = (ushort)data.Length;
            SendBuffer[0] = (byte)(size & 0xFF);
            SendBuffer[1] = (byte)((size >> 8) & 0xFF);

            var sizeWithHeader = data.Length + PacketHeaderSize;
            if (sizeWithHeader > SendBuffer.Length)
                throw new InvalidOperationException("Data is too big");

            data.CopyTo(SendBuffer.AsSpan(PacketHeaderSize));
            _bytesToSent = sizeWithHeader;
            _sentBytes = 0;
        }

        public bool PollWrite()
        {
            if (_sentBytes >= _bytesToSent)
                return false;

            try
            {
                var sentBytes = Client.Send(SendBuffer, _sentBytes, _bytesToSent - _sentBytes, SocketFlags.None);
                _sentBytes += sentBytes;
                return true;
            }
            catch (SocketException e)
            {
                if (e.SocketErrorCode != SocketError.TimedOut)
                    throw;

                return false;
            }
        }

        public bool PollRead([MaybeNullWhen(false)] out byte[] result)
        {
            result = null;

            if (_bytesReceived < PacketHeaderSize)
            {
                try
                {
                    _bytesReceived += Client.Receive(ReceiveBuffer, 0, PacketHeaderSize - _bytesReceived,
                        SocketFlags.None);
                }
                catch (SocketException e)
                {
                    if (e.SocketErrorCode != SocketError.TimedOut)
                        throw;

                    return false;
                }

                if (_bytesReceived < PacketHeaderSize)
                    return false;

                var packetSize = ReceiveBuffer[0] | (ReceiveBuffer[1] << 8);
                _bytesToReceive = packetSize + PacketHeaderSize;
            }

            try
            {
                _bytesReceived += Client.Receive(ReceiveBuffer, _bytesReceived, _bytesToReceive - _bytesReceived,
                    SocketFlags.None);
            }
            catch (SocketException e)
            {
                if (e.SocketErrorCode != SocketError.TimedOut)
                    throw;

                return false;
            }

            if (_bytesReceived != _bytesToReceive)
                return false;

            result = new byte[_bytesToReceive - PacketHeaderSize];
            Array.Copy(ReceiveBuffer, 2, result, 0, result.Length);
            _bytesReceived = 0;
            _bytesToReceive = 0;
            return true;
        }

        public void Dispose()
        {
            try
            {
                Client.Dispose();
            }
            catch (SocketException)
            {
            }
        }
    }
}