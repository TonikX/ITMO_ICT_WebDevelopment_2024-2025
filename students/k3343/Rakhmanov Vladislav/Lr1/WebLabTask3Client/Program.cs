using System;
using System.Net.Http;
using System.Threading.Tasks;

namespace HttpClientExample
{
    class Program
    {
        static async Task Main(string[] args)
        {
            const string url = "http://localhost:8080";

            using (HttpClient client = new HttpClient())
            {
                HttpResponseMessage response = await client.GetAsync(url);
                response.EnsureSuccessStatusCode();

                string responseBody = await response.Content.ReadAsStringAsync();
                Console.WriteLine(responseBody);
            }
        }
    }
}
