using System.Collections.Concurrent;
using System.Diagnostics;
using System.Diagnostics.CodeAnalysis;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Text.Unicode;

namespace Server;

class Program
{
    static async Task Main(string[] args)
    {
        var listenPort = 22102;
        var socket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
        socket.Bind(new IPEndPoint(IPAddress.Any, listenPort));
        socket.Listen(10);

        var webServer = new WebServer(socket);
        var packets = new List<WebServer.ReceivedPacket>();

        while (true)
        {
            webServer.FlushPackets(packets);
            foreach (var packet in packets)
            {
                var sender = packet.Sender;
                var message = UTF32Encoding.UTF32.GetString(packet.Value);
                var fullMessageText = $"{sender.Address}:{sender.Port} : {message}";
                Console.WriteLine(fullMessageText);

                var dataToSend = UTF32Encoding.UTF32.GetBytes(fullMessageText);
                webServer.SendPacket(ip => !Equals(ip, sender), dataToSend);
            }

            packets.Clear();
        }
    }

    private class WebServer
    {
        private readonly Socket _socket;
        private readonly ConcurrentDictionary<EndPoint, Connection> _connections = new();
        private readonly ConcurrentQueue<ReceivedPacket> _packets = new();

        private bool _isWaitingForConnection;

        public WebServer(Socket socket)
        {
            _socket = socket;
            var thread = new Thread(() =>
            {
                while (true)
                {
                    PollConnections();
                    PoolSend();
                    PoolReceive();
                }
            });

            thread.Start();
        }

        private void PollConnections()
        {
            if (_isWaitingForConnection)
                return;

            _isWaitingForConnection = true;
            var socketAsyncEventArgs = new SocketAsyncEventArgs();
            socketAsyncEventArgs.Completed += OnAccept;
            var isAsync = _socket.AcceptAsync(socketAsyncEventArgs);
            if (!isAsync)
                OnAccept(null, socketAsyncEventArgs);
        }

        private void PoolSend()
        {
            foreach (var connection in _connections.Values)
            {
                try
                {
                    if (connection.IsSending)
                        connection.PollWrite();
                }
                catch (SocketException e)
                {
                    if (e.SocketErrorCode == SocketError.ConnectionReset)
                        RemoveDisconnectedClient(connection);
                    else
                        throw;
                }

                if (!connection.Client.Connected)
                    RemoveDisconnectedClient(connection);
            }
        }

        private void OnAccept(object? sender, SocketAsyncEventArgs e)
        {
            if (e.SocketError != SocketError.Success)
            {
                Console.WriteLine(e.SocketError);
                return;
            }

            if (e.AcceptSocket == null)
            {
                Console.WriteLine("Accept socket is null");
                return;
            }

            var connection = new Connection(e.AcceptSocket);
            connection.Client.ReceiveTimeout = 1;
            connection.Client.SendTimeout = 1;
            _connections.TryAdd(connection.Client.RemoteEndPoint, connection);
            _isWaitingForConnection = false;
        }

        public void FlushPackets(List<ReceivedPacket> packets)
        {
            while (_packets.TryDequeue(out var packet))
                packets.Add(packet);
        }

        private void PoolReceive()
        {
            foreach (var connection in _connections.Values)
            {
                try
                {
                    while (connection.PollRead(out var result))
                        _packets.Enqueue(new ReceivedPacket(connection.Client.RemoteEndPoint as IPEndPoint, result));
                }
                catch (SocketException e)
                {
                    if (e.SocketErrorCode == SocketError.ConnectionReset)
                        RemoveDisconnectedClient(connection);
                    else
                        throw;
                }
            }
        }

        private void RemoveDisconnectedClient(Connection connection)
        {
            Console.WriteLine($"Client {connection.Client.RemoteEndPoint} disconnected");
            _connections.TryRemove(connection.Client.RemoteEndPoint, out _);
        }

        public void SendPacket(Predicate<IPEndPoint> receiverFilter, Span<byte> data)
        {
            foreach (var connection in _connections.Values)
            {
                try
                {
                    if (receiverFilter(connection.Client.RemoteEndPoint as IPEndPoint))
                        connection.Send(data);
                }
                catch (SocketException e)
                {
                    if (e.SocketErrorCode == SocketError.ConnectionReset)
                        RemoveDisconnectedClient(connection);
                    else
                        throw;
                }
            }
        }

        public class ReceivedPacket
        {
            public IPEndPoint Sender;
            public byte[] Value;

            public ReceivedPacket(IPEndPoint sender, byte[] value)
            {
                Sender = sender;
                Value = value;
            }
        }
    }

    private class Connection : IDisposable
    {
        private const int PacketHeaderSize = 2;

        public readonly Socket Client;
        public readonly byte[] ReceiveBuffer = new byte[1024 * 8];
        public readonly byte[] SendBuffer = new byte[1024 * 8];

        public bool IsSending => _sentBytes < _bytesToSent;

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