# Задание 2

Реализовать клиентскую и серверную часть приложения. Клиент запрашивает выполнение математической операции, параметры
которой вводятся с клавиатуры. Сервер обрабатывает данные и возвращает результат клиенту.

Варианты операций:

- Теорема Пифагора.
- Решение квадратного уравнения.
- Поиск площади трапеции.
- Поиск площади параллелограмма.

Порядок выбора варианта: Выбирается по порядковому номеру в журнале (пятый студент получает вариант 1 и т.д.).

# Требования

- Обязательно использовать библиотеку socket.
- Реализовать с помощью протокола TCP.

# Ход работы

Мой номер 21, мой вариант 1. Теорема Пифагора.
В начале всё реализовал как в первом задании, но только потом понял,
что нужно сделать не на UDP, а на TCP. Самым простым оказалось использовать ядро,
которое написано поверх TCP для заданий 3,4,5. Поэтому я решил использовать его и для этого задания.
Описание ядра есть в следующем задании.
Вот код сервера который относится конкретно к этому заданию:

```csharp
webServer.RegisterRouteGet("/math",
    async arguments =>
    {
        if (!arguments.TryGetValue("a", out var aRaw) || !int.TryParse(aRaw, out var a))
            return new HttpResponse("", HttpResponse.Type.BadRequest);
        
        if (!arguments.TryGetValue("b", out var bRaw) || !int.TryParse(bRaw, out var b))
            return new HttpResponse("", HttpResponse.Type.BadRequest);
        
        var cValue = (float)Math.Sqrt(a * a + b * b);
        return new HttpResponse(cValue.ToString(), HttpResponse.Type.Success);
    });
```

Клиент просто отправляет HTTP запросы к серверу, на которые он отвечает,
как на обычные HTTP запросы. Но всё это написано поверх голого сокета, что соответствует питоновскому socket
и с помощью протокола TCP.

# Листинг кода

#### Сервер

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
        webServer.RegisterRouteGet("/math",
            async arguments =>
            {
                if (!arguments.TryGetValue("a", out var aRaw) || !int.TryParse(aRaw, out var a))
                    return new HttpResponse("", HttpResponse.Type.BadRequest);

                if (!arguments.TryGetValue("b", out var bRaw) || !int.TryParse(bRaw, out var b))
                    return new HttpResponse("", HttpResponse.Type.BadRequest);
                
                var cValue = (float)Math.Sqrt(a * a + b * b);
                return new HttpResponse(cValue.ToString(), HttpResponse.Type.Success);
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

#### Клиент

```csharp
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
```