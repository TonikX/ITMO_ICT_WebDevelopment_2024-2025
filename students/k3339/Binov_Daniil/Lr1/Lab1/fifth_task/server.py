import socket
import urllib.parse


class MyHTTPServer:
    def __init__(self, host='localhost', port=8080):
        self.host = host
        self.port = port
        self.data = {}

    def serve_forever(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.host, self.port))
            server_socket.listen(5)
            print(f'Server running on http://{self.host}:{self.port}')
            while True:
                client_socket, addr = server_socket.accept()
                with client_socket:
                    print(f'Connection from {addr}')
                    self.serve_client(client_socket)

    def serve_client(self, client_socket):
        request = client_socket.recv(1024).decode('utf-8')
        print(f'Request: {request}')
        response = self.handle_request(request)
        client_socket.sendall(response)

    def handle_request(self, request):
        headers = request.split('\n')
        request_line = headers[0].split()
        method = request_line[0]
        path = request_line[1]

        if method == 'POST':
            return self.handle_post(path, headers)
        elif method == 'GET':
            return self.handle_get()
        else:
            return self.send_response('405 Method Not Allowed', 'Method Not Allowed')

    def handle_post(self, path, headers):
        body = headers[-1]
        parsed_body = urllib.parse.parse_qs(body)

        discipline = parsed_body.get('discipline', [''])[0]
        grade = parsed_body.get('grade', [''])[0]

        if discipline and grade:
            self.data[discipline] = grade
            return self.send_response('200 OK', 'Data received')
        else:
            return self.send_response('400 Bad Request', 'Invalid data')

    def handle_get(self):
        html_content = '<html><body><h1>Grades</h1><ul>'
        for discipline, grade in self.data.items():
            html_content += f'<li>{discipline}: {grade}</li>'
        html_content += '</ul></body></html>'
        return self.send_response('200 OK', html_content)

    def send_response(self, status_code, body):
        response = f'HTTP/1.1 {status_code}\r\n'
        response += 'Content-Type: text/html\r\n'
        response += f'Content-Length: {len(body)}\r\n'
        response += '\r\n' + body
        return response.encode('utf-8')


if __name__ == '__main__':
    host = '127.0.0.1'
    port = 8080
    serv = MyHTTPServer(host, port)
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Server stopped.")
