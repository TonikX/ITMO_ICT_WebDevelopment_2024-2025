using System;
using System.IO;
using System.Net;
using System.Text;

namespace HttpServer
{
    class Program
    {
        static void Main(string[] args)
        {
            const string prefix = "http://localhost:8080/";

            using (HttpListener listener = new HttpListener())
            {
                listener.Prefixes.Add(prefix);
                listener.Start();
                Console.WriteLine("Сервер запущен. Ожидание подключений...");

                while (true)
                {
                    HttpListenerContext context = listener.GetContext();
                    HttpListenerRequest request = context.Request;
                    HttpListenerResponse response = context.Response;

                    string filePath = "C:/Users/guign/Source/Repos/web-lab-1/WebLabTask3Server/index.html";
                    if (File.Exists(filePath))
                    {
                        string content = File.ReadAllText(filePath, Encoding.UTF8);
                        byte[] buffer = Encoding.UTF8.GetBytes(content);

                        response.ContentLength64 = buffer.Length;
                        response.ContentType = "text/html";
                        response.OutputStream.Write(buffer, 0, buffer.Length);
                    }
                    else
                    {
                        response.StatusCode = (int)HttpStatusCode.NotFound;
                        byte[] buffer = Encoding.UTF8.GetBytes("<html><body><h1>404 - File Not Found</h1></body></html>");
                        response.ContentLength64 = buffer.Length;
                        response.ContentType = "text/html";
                        response.OutputStream.Write(buffer, 0, buffer.Length);
                    }

                    response.OutputStream.Close();
                }
            }
        }
    }
}
