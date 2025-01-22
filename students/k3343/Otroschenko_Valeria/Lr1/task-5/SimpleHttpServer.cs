using System.Net;
using System.Net.Sockets;
using System.Text;

namespace ConsoleApp1.task_5;

class SimpleHttpServer
{
    private static Dictionary<string, List<string>> _grades = new Dictionary<string, List<string>>();
    private const string IpAddress = "127.0.0.1";
    private const int Port = 8080;

    public static void Main()
    {
        IPAddress ip = IPAddress.Parse(IpAddress);
        TcpListener listener = new TcpListener(ip, Port);
        listener.Start();

        Console.WriteLine($"Сервер запущен на {IpAddress}:{Port}. Ожидание запросов...");

        while (true)
        {
            TcpClient client = listener.AcceptTcpClient();
            Console.WriteLine("Новый клиент подключен.");

            HandleRequest(client);
            client.Close();
        }
    }

    private static void HandleRequest(TcpClient client)
    {
        NetworkStream stream = client.GetStream();
        StreamReader reader = new StreamReader(stream);
        StreamWriter writer = new StreamWriter(stream) { AutoFlush = true };

        string? requestLine = reader.ReadLine();
        Console.WriteLine($"Получен запрос: {requestLine}");

        int contentLength = 0;
        string? line;
        while (!string.IsNullOrEmpty(line = reader.ReadLine()))
        {
            if (line.StartsWith("Content-Length:"))
            {
                contentLength = int.Parse(line.Substring("Content-Length:".Length).Trim());
            }
        }

        if (requestLine != null && requestLine.StartsWith("GET"))
        {
            SendHtmlResponse(writer, null);
        }
        else if (requestLine != null && requestLine.StartsWith("POST"))
        {
            string? errorMessage = HandlePostRequest(reader, contentLength);
            SendHtmlResponse(writer, errorMessage);
        }
    }

    private static void SendHtmlResponse(StreamWriter writer, string? errorMessage)
    {
        string htmlContent = "<html><body><h1>Grades by Subject</h1><table border='1'><tr><th>Subject</th><th>Grades</th></tr>";

        foreach (var grade in _grades)
        {
            string gradesString = string.Join(", ", grade.Value);
            htmlContent += $"<tr><td>{grade.Key}</td><td>{gradesString}</td></tr>";
        }

        htmlContent += "</table>";

        if (!string.IsNullOrEmpty(errorMessage))
        {
            htmlContent += $"<p style='color: red;'>{errorMessage}</p>";
        }

        htmlContent += "<br/><form method='POST'><label>Subject: </label><input type='text' name='subject'/><br/><label>Grade: </label><input type='text' name='grade'/><br/><input type='submit' value='Add'/></form></body></html>";

        writer.WriteLine("HTTP/1.1 200 OK");
        writer.WriteLine("Content-Type: text/html");
        writer.WriteLine($"Content-Length: {Encoding.UTF8.GetByteCount(htmlContent)}");
        writer.WriteLine();
        writer.WriteLine(htmlContent);
    }

    private static string? HandlePostRequest(StreamReader reader, int contentLength)
    {
        char[] buffer = new char[contentLength];
        reader.Read(buffer, 0, contentLength);
        string body = new string(buffer);
        Console.WriteLine($"POST тело: {body}");

        var data = ParsePostData(body);

        if (!data.ContainsKey("subject") || string.IsNullOrEmpty(data["subject"]))
        {
            return "Subject cannot be empty.";
        }
        if (!data.ContainsKey("grade") || string.IsNullOrEmpty(data["grade"]))
        {
            return "Grade cannot be empty.";
        }

        string subject = data["subject"];
        string grade = data["grade"];

        if (_grades.ContainsKey(subject))
        {
            _grades[subject].Add(grade);
        }
        else
        {
            _grades[subject] = new List<string> { grade };
        }

        Console.WriteLine($"Added/Updated subject: {subject}, grade: {grade}");
        return null;
    }

    private static Dictionary<string, string> ParsePostData(string body)
    {
        var data = new Dictionary<string, string>();

        string[] pairs = body.Split('&');
        foreach (var pair in pairs)
        {
            string[] keyValue = pair.Split('=');
            if (keyValue.Length == 2)
            {
                string key = Uri.UnescapeDataString(keyValue[0]);
                string value = Uri.UnescapeDataString(keyValue[1]);
                data[key] = value;
            }
        }
        return data;
    }
}