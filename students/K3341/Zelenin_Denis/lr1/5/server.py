import socket
from urllib.parse import parse_qs


class MyHTTPServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.data = {}

    def serve_forever(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, self.port))
        server.listen()
        print(f"Сервер запущен {self.host} {self.port}")
        while True:
            conn, _ = server.accept()
            self.serve_client(conn)

    def serve_client(self, conn):
        request = conn.recv(1024).decode('utf-8')
        if not request:
            return
        method, path, headers, body = self.parse_request(request)
        response = self.handle_request(method, path, headers, body)
        conn.sendall(response)

    def parse_request(self, request):
        lines = request.split('\r\n')
        method, path, version = lines[0].split(' ')
        headers = self.parse_headers(lines[1:])
        body = lines[-1] if method == "POST" else ""
        return method, path, headers, body

    def parse_headers(self, lines):
        headers = {}
        for line in lines:
            if line == "":
                break
            key, value = line.split(": ", 1)
            headers[key] = value
        return headers

    def handle_request(self, method, path, headers, body):
        if method == "GET":
            return self.handle_get(path)
        elif method == "POST":
            return self.handle_post(path, body)
        else:
            return self.send_response(405, "Method Not Allowed", "Method not supported")

    def handle_get(self, path):
        html_content = "<html><body><h1>Журнал оценок</h1><ul>"
        for subject, grades in self.data.items():
            html_content += f"<li>{subject}: {', '.join(map(str, grades))}</li>"
        html_content += "</ul></body></html>"
        return self.send_response(200, "OK", html_content, content_type="text/html")

    def handle_post(self, path, body):
        parsed_body = parse_qs(body)
        subject = parsed_body.get('subject', [''])[0]
        grade = parsed_body.get('grade', [''])[0]

        if subject and grade:
            self.data.setdefault(subject, []).append(grade)
            return self.send_response(200, "OK", "Data added successfully")
        else:
            return self.send_response(400, "Bad Request", "Missing subject or grade")

    def send_response(self, status_code, reason, content, content_type="text/plain"):
        response = f"HTTP/1.1 {status_code} {reason}\r\n"
        response += f"Content-Type: {content_type}\r\n"
        response += f"Content-Length: {len(content.encode('utf-8'))}\r\n"
        response += "\r\n"
        response += content
        return response.encode('utf-8')


if __name__ == '__main__':
    host = '127.0.0.1'
    port = 8080
    server = MyHTTPServer(host, port)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nСервер остановлен")
