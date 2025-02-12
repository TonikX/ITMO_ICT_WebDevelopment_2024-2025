## Задание №4. Многопользовательский чат

### Описание: 
Реализовать двухпользовательский или многопользовательский чат. Для максимального количества баллов реализуйте многопользовательский чат.

### Требования:
* Обязательно использовать библиотеку socket.
* Для многопользовательского чата необходимо использовать библиотеку threading.

### Реализация:

* Протокол TCP: 100% баллов.
* Протокол UDP: 80% баллов.
* Для UDP используйте threading для получения сообщений на клиенте.
* Для TCP запустите клиентские подключения и обработку сообщений от всех пользователей в потоках. Не забудьте сохранять пользователей, чтобы отправлять им сообщения.

### Листинг кода:
#### server.py
```
import socket
import sys


class MyHTTPServer:
    def __init__(self, host, port, name):
        self.host = host
        self.port = port
        self.name = name
        self.grades = {}

    def serve_forever(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((self.host, self.port))
            server_socket.listen(1)
            print(f'Server started on {self.host}:{self.port}')
            print("http://localhost:8080")

            while True:
                client_socket, client_address = server_socket.accept()
                self.serve_client(client_socket)

    def serve_client(self, client_socket):
        request = client_socket.recv(1024).decode('utf-8')
        method, url, version = self.parse_request(request)
        headers, body = self.parse_headers(request)

        if method == 'GET':
            response_body = self.get_grades()
            self.send_response(client_socket, '200 OK', response_body)
        elif method == 'POST':
            self.add_grade(body)
            self.send_response(client_socket, '200 OK', '<html><body><h1>Grade Added</h1></body></html>')
        else:
            self.send_response(client_socket, '405 Method Not Allowed',
                               '<html><body><h1>Method Not Allowed</h1></body></html>')

    def parse_request(self, request):
        request_line = request.splitlines()[0]
        method, url, version = request_line.split(' ')
        return method, url, version

    def parse_headers(self, request):
        headers = {}
        lines = request.splitlines()
        body_index = request.index('\r\n\r\n') + 4
        headers_body = lines[1:]

        for line in headers_body:
            if line == '':
                break
            header, value = line.split(': ', 1)
            headers[header] = value

        body = request[body_index:]
        return headers, body

    def handle_request(self, method, url, body):
        if method == 'GET':
            return self.get_grades()
        elif method == 'POST':
            self.add_grade(body)
            return '<html><body><h1>Grade Added</h1></body></html>'
        else:
            return '<html><body><h1>Method Not Allowed</h1></body></html>'

    def get_grades(self):
        html_response = '<html><body><h1>Grades</h1><ul>'
        for discipline, grade in self.grades.items():
            html_response += f'<li>{discipline}: {grade}</li>'
        html_response += '</ul></body></html>'
        return html_response

    def add_grade(self, body):
        params = body.split('&')
        discipline = None
        grade = None
        for param in params:
            key, value = param.split('=')
            if key == 'discipline':
                discipline = value
            elif key == 'grade':
                grade = value
        if discipline and grade:
            self.grades[discipline] = grade

    def send_response(self, client_socket, status, body):
        response = f'HTTP/1.1 {status}\r\nContent-Type: text/html\r\nContent-Length: {len(body)}\r\n\r\n{body}'
        client_socket.sendall(response.encode('utf-8'))

if __name__ == '__main__':
    host = "localhost"
    port = 8080
    name = "GraduateWeb"
    serv = MyHTTPServer(host, port, name)
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        pass
```

#### client.py
``` 
import socket

def send_get_request(host, port):
    request = "GET / HTTP/1.1\r\nHost: {}\r\n\r\n".format(host)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        client_socket.sendall(request.encode('utf-8'))
        response = client_socket.recv(4096).decode('utf-8')
        print("GET response: \n", response)

def send_post_request(host, port, discipline, grade):
    body = "discipline={}&grade={}".format(discipline, grade)
    request = "POST / HTTP/1.1\r\nHost: {}\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: {}\r\n\r\n{}".format(host, len(body), body)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        client_socket.sendall(request.encode('utf-8'))
        response = client_socket.recv(4096).decode('utf-8')
        print("POST response: \n", response)

if __name__ == '__main__':
    host = "localhost"
    port = 8080

    # Отправка POST запроса для добавления новой оценки
    send_post_request(host, port, "Math", "4")
    send_post_request(host, port, "WEB", "5")
    send_post_request(host, port, "FRONT", "5")
    send_post_request(host, port, "DATABASE", "5")

    # Отправка GET запроса для получения списка всех оценок
    send_get_request(host, port)
```

### Пояснение:
При реализации было принято решение сделать многопользовательский чат с применением TCP протокола. У клиента есть возможность отправлять сообщения, видеть всех учатников чата, а также при желании выходить из чата с помощью кодового слова "exit". Если говорить о серверной части, было реализовано запоминание каждого пользователя в словаре (с его подключением и адресом), обработка входящих сообщений и перенаправление остальным клиентам, удаление клиента из чата и информирование об этом остальных, а также запоминание всех входящих и выходящих клиентов путем простого вывода данной информации в консоль. Каждый клиент может видеть, кто сейчас онлайн, кто покинул чат, а кто отправил каждое сообщение