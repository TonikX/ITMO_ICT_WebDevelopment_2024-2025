# Задание 3

Реализовать серверную часть приложения. Клиент подключается к серверу,
и в ответ получает HTTP-сообщение, содержащее HTML-страницу, которая сервер подгружает из файла index.html.

# Требования

- Обязательно использовать библиотеку socket.

# Ход работы

Клиент здесь не нужен, так как в его роли выступает всё, что может отправлять HTTP-запросы, к примеру, Postman.
Здесь я сделал небольшое мини-ядро для http сервера, на котором я по итогу реализовал 3, 4 и 5 задания.

Реализовано получение аргументов из url и только оттуда, обращения к разным эндпоинтам по разным методам
(только Get и Post), а также отправка валидного ответа с корректными статус кодами.

Кроме кода ядра для выполнения этого задания понадобилось только:

```csharp
webServer.RegisterRouteGet("/index.html",
    async arguments =>
    {
        return new HttpResponse(await File.ReadAllTextAsync("index.html"), HttpResponse.Type.Success);
    });
```

# Листинг кода

```csharp
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
        socket.Bind(new IPEndPoint(IPAddress.Any, listenPort));
        socket.Listen(10);

        var webServer = new WebServer(socket);
        webServer.RegisterRouteGet("/index.html",
            async arguments =>
            {
                return new HttpResponse(await File.ReadAllTextAsync("index.html"), HttpResponse.Type.Success);
            });

        while (true)
        {
            webServer.PollConnection();
            webServer.PollRequests();
            webServer.PollRequestProcessing();
        }
    }

    private class WebServer
    {
        private readonly Socket _socket;
        private readonly Dictionary<EndPoint, Connection> _connections = new();

        private readonly Dictionary<string, Func<Dictionary<string, string>, Task<HttpResponse>>>
            _routeHandlersGet = new();

        private readonly Dictionary<string, Func<Dictionary<string, string>, Task<HttpResponse>>>
            _routeHandlersPost = new();

        private bool _isWaitingForConnection;

        public WebServer(Socket socket)
        {
            _socket = socket;
        }

        public void PollConnection()
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

        public void PollRequests()
        {
            foreach (var connection in _connections.ToArray())
            {
                var receivingTask = connection.Value.ReceivingTask;
                if (receivingTask is null)
                {
                    receivingTask = connection.Value.Client.ReceiveAsync(connection.Value.Buffer);
                    connection.Value.ReceivingTask = receivingTask;
                    continue;
                }

                if (!receivingTask.IsCompleted)
                    continue;

                connection.Value.ReceivingTask = null;

                try
                {
                    try
                    {
                        var receivedBytesCount = receivingTask.Result;
                        connection.Value.FlushToStream(receivedBytesCount);
                    }
                    catch (AggregateException e)
                    {
                        throw e.InnerException!;
                    }
                }
                catch (SocketException e)
                {
                    if (e.SocketErrorCode != SocketError.ConnectionReset)
                        Console.WriteLine(e);
                    connection.Value.Dispose();
                    _connections.Remove(connection.Key);
                }
                catch (Exception e)
                {
                    Console.WriteLine(e);
                    connection.Value.Dispose();
                    _connections.Remove(connection.Key);
                }
            }
        }

        public void PollRequestProcessing()
        {
            foreach (var connection in _connections.ToArray())
            {
                var requestProcessingTask = connection.Value.RequestProcessingTask;
                if (requestProcessingTask is null)
                {
                    connection.Value.RequestProcessingTask = ProcessRequest(connection.Value.RequestReader);
                    continue;
                }

                if (!requestProcessingTask.IsCompleted)
                    continue;

                connection.Value.RequestProcessingTask = null;
                connection.Value.ResetBuffer();

                try
                {
                    var response = requestProcessingTask.Result;
                    connection.Value.Client.Send(response);
                }
                catch (Exception e)
                {
                    Console.WriteLine(e);
                    connection.Value.Dispose();
                    _connections.Remove(connection.Key);
                }
            }
        }

        public void RegisterRouteGet(string route, Func<Dictionary<string, string>, Task<HttpResponse>> handler)
        {
            _routeHandlersGet.Add(route, handler);
        }

        public void RegisterRoutePost(string route, Func<Dictionary<string, string>, Task<HttpResponse>> handler)
        {
            _routeHandlersPost.Add(route, handler);
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
            _connections.Add(connection.Client.RemoteEndPoint, connection);
            _isWaitingForConnection = false;
        }

        private async Task<byte[]> ProcessRequest(StreamReader connectionRequestReader)
        {
            var firstLine = await connectionRequestReader.ReadLineAsync();
            if (firstLine == null)
                return Encoding.ASCII.GetBytes("HTTP/1.1 400 Bad Request\r\nContent-Length: 0\r\n\r\n");

            var requestParts = firstLine.Split(' ');
            if (requestParts.Length != 3 || (requestParts[0] != "GET" && requestParts[0] != "POST"))
                return Encoding.ASCII.GetBytes("HTTP/1.1 400 Bad Request\r\nContent-Length: 0\r\n\r\n");

            var pathAndArguments = requestParts[1].Split('?');
            var path = pathAndArguments[0];
            var headers = new List<string>();
            var maxHeadersCount = 100;
            while (maxHeadersCount-- > 0)
            {
                var header = await connectionRequestReader.ReadLineAsync();
                if (string.IsNullOrEmpty(header))
                    break;

                headers.Add(header);
            }

            if (maxHeadersCount == 0)
                return Encoding.ASCII.GetBytes("HTTP/1.1 400 Bad Request\r\nContent-Length: 0\r\n\r\n");

            Func<Dictionary<string, string>, Task<HttpResponse>> handler = null;
            if (requestParts[0] == "GET" && !_routeHandlersGet.TryGetValue(path, out handler))
                return Encoding.ASCII.GetBytes("HTTP/1.1 404 Not Found\r\nContent-Length: 0\r\n\r\n");

            if (requestParts[0] == "POST" && !_routeHandlersPost.TryGetValue(path, out handler))
                return Encoding.ASCII.GetBytes("HTTP/1.1 404 Not Found\r\nContent-Length: 0\r\n\r\n");

            var argumentsRaw = pathAndArguments.Length > 1 ? pathAndArguments[1] : "";
            var arguments = argumentsRaw.Split('&')
                .Where(e => !string.IsNullOrWhiteSpace(e)).Select(x => x.Split('='))
                .ToDictionary(x => x[0], x => x[1]);
            try
            {
                Console.WriteLine($"Processing request: {path} with method {requestParts[0]}");
                var response = await handler(arguments);
                return Encoding.ASCII.GetBytes(
                    $"HTTP/1.1 {response.GetStatusString()}\r\nContent-Length: {response.Content.Length}\r\n\r\n{response.Content}");
            }
            catch (Exception e)
            {
                Console.WriteLine(e);
                return Encoding.ASCII.GetBytes("HTTP/1.1 500 Internal Server Error\r\nContent-Length: 0\r\n\r\n");
            }
        }
    }

    private class Connection : IDisposable
    {
        public readonly Socket Client;
        public readonly byte[] Buffer = new byte[1024 * 8];
        public readonly StreamReader RequestReader;
        public Task<int> ReceivingTask;
        public Task<byte[]> RequestProcessingTask;

        public int ReceivedBytesCount { get; private set; }
        private readonly ProducerConsumerStream _receivedStream;

        public Connection(Socket client)
        {
            Client = client;
            _receivedStream = new ProducerConsumerStream();
            RequestReader = new StreamReader(_receivedStream, Encoding.ASCII);
        }

        public void FlushToStream(int count)
        {
            ReceivedBytesCount += count;
            _receivedStream.Write(Buffer, 0, count);
            _receivedStream.Flush();
        }

        public void ResetBuffer()
        {
            Array.Clear(Buffer, 0, Buffer.Length);
            _receivedStream.Flush();
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

    public class HttpResponse
    {
        public string Content { get; }
        public Type Status { get; }

        public HttpResponse(string content, Type status)
        {
            Content = content;
            Status = status;
        }

        public string GetStatusString()
        {
            return Status switch
            {
                Type.Success => "200 OK",
                Type.BadRequest => "400 Bad Request",
                Type.NotFound => "404 Not Found",
                Type.InternalServerError => "500 Internal Server Error",
                _ => throw new ArgumentOutOfRangeException()
            };
        }

        public enum Type
        {
            Success,
            BadRequest,
            NotFound,
            InternalServerError
        }
    }
}
```