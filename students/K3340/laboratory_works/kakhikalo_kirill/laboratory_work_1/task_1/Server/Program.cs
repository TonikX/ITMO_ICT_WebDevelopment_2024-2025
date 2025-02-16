using System.Collections.Concurrent;
using System.Net;
using System.Net.Sockets;
using System.Text;

namespace Server;

class Program
{
    static async Task Main(string[] args)
    {
        var listenPort = 22102;
        var socket = new Socket(AddressFamily.InterNetwork, SocketType.Dgram, ProtocolType.Udp);
        socket.Bind(new IPEndPoint(IPAddress.Any, listenPort));

        // https://stackoverflow.com/questions/38191968/c-sharp-udp-an-existing-connection-was-forcibly-closed-by-the-remote-host
        const int SIO_UDP_CONNRESET = -1744830452;
        socket.IOControl((IOControlCode)SIO_UDP_CONNRESET, new byte[] { 0, 0, 0, 0 }, null);
        socket.SetSocketOption(SocketOptionLevel.IP, SocketOptionName.PacketInformation, true);

        EndPoint client = new IPEndPoint(IPAddress.Any, listenPort);

        var clients = new ConcurrentDictionary<EndPoint, Connection>();
        var buffer = new byte[1024];
        while (true)
        {
            var received = await socket.ReceiveFromAsync(buffer, client);
            if (!clients.TryGetValue(received.RemoteEndPoint, out var connection))
            {
                connection = new Connection(received.RemoteEndPoint);
                clients.TryAdd(received.RemoteEndPoint, connection);
            }

            var isTargetKeysFound = Receive(connection, buffer.AsSpan(0, received.ReceivedBytes));
            if (!isTargetKeysFound)
                continue;

            Console.WriteLine($"Received: {connection.ReceivedData} from {connection.Client}");
            var dataToSend = Encoding.UTF8.GetBytes("Hello, client");
            connection.SendingData = dataToSend;
            connection.SentBytes = 0;
            await Send(socket, connection);
        }
    }

    private static async Task Send(Socket socket, Connection connection)
    {
        var bufferToSend = connection.SendingData.AsMemory(connection.SentBytes,
            connection.SendingData.Length - connection.SentBytes);
        connection.SentBytes += await socket.SendToAsync(bufferToSend, connection.Client);
    }

    private static bool Receive(Connection connection, ReadOnlySpan<byte> receivedBytes)
    {
        connection.ReceivedData.Append(Encoding.UTF8.GetString(receivedBytes));

        const string target = "Hello, server";
        if (connection.ReceivedData.Length < target.Length)
            return false;

        var receivedString = connection.ReceivedData.ToString();
        return receivedString.Contains(target);
    }

    private class Connection
    {
        public readonly EndPoint Client;
        public readonly StringBuilder ReceivedData = new();
        public int SentBytes;
        public byte[]? SendingData;

        public Connection(EndPoint client)
        {
            Client = client;
        }
    }
}