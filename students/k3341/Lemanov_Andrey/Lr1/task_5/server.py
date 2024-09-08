import socket
import sys
from urllib.parse import urlparse, parse_qs


class MyHTTPServer:
    def __init__(self, host='localhost', port=8080):
        self.host = host
        self.port = port
        self.grades = {}

    def serve_forever(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.host, self.port))
            server_socket.listen()
            print(f'Server running on http://{self.host}:{self.port}')
            while True:
                client_socket, _ = server_socket.accept()
                self.serve_client(client_socket)

    def serve_client(self, client_socket):
        with client_socket:
            request = client_socket.recv(1024).decode()
            print(f'Received request:\n{request}')
            request_line, headers = self.parse_request(request)
            self.handle_request(request_line, headers, client_socket)

    def parse_request(self, request):
        lines = request.splitlines()
        request_line = lines[0]
        headers = self.parse_headers(lines[1:])
        return request_line, headers

    def parse_headers(self, lines):
        headers = {}
        for line in lines:
            if line == '':
                break
            key, value = line.split(': ', 1)
            headers[key] = value
        return headers

    def handle_request(self, request_line, headers, client_socket):
        method, url, _ = request_line.split()
        parsed_url = urlparse(url)
        path = parsed_url.path
        query = parse_qs(parsed_url.query)

        if method == 'POST':
            self.handle_post(query)
            self.send_response(client_socket, 200, 'OK', 'Data received')
        elif method == 'GET':
            response_body = self.handle_get()
            self.send_response(client_socket, 200, 'OK', response_body)
        else:
            self.send_response(client_socket, 405, 'Method Not Allowed', '')

    def handle_post(self, query):
        discipline = query.get('discipline', [''])[0]
        grade = query.get('grade', [''])[0]
        if discipline and grade:
            self.grades[discipline] = grade

        print(discipline, grade)

    def handle_get(self):
        html_content = '<html><body><h1>Grades</h1><ul>'
        for discipline, grade in self.grades.items():
            html_content += f'<li>{discipline}: {grade}</li>'
        html_content += '</ul></body></html>'
        return html_content

    def send_response(self, client_socket, status_code, reason, body):
        response_line = f'HTTP/1.1 {status_code} {reason}\r\n'
        headers = 'Content-Type: text/html\r\n'
        headers += f'Content-Length: {len(body)}\r\n'
        headers += '\r\n'  # End of headers
        response = response_line + headers + body
        client_socket.sendall(response.encode())


if __name__ == '__main__':
    host = 'localhost'
    port = 8080
    name = 'Simple HTTP Server'
    serv = MyHTTPServer(host, port)
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
