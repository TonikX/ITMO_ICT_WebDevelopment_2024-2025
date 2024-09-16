import os
from server import Server

class HTTPServer(Server):
    def send_html_response(self):
        data, conn = self.handle_client()

        html_file = 'index.html'
        if os.path.exists(html_file):
            with open(html_file, 'r') as file:
                html_content = file.read()
        else:
            html_content = "<h1>404 Not Found</h1>"

        http_response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n{html_content}"

        conn.sendall(http_response.encode())
        print("Sent HTML page to client")

        conn.close()

if __name__ == "__main__":
    server = HTTPServer(protocol_type="TCP")
    print("HTTP Server is running...")
    server.send_html_response()
    server.close()
