## Задание 5:
Написать простой веб-сервер для обработки GET и POST HTTP-запросов с помощью библиотеки socket в Python.

### Задание:

Сервер должен:
Принять и записать информацию о дисциплине и оценке по дисциплине.
Отдать информацию обо всех оценках по дисциплинам в виде HTML-страницы.


`Server's code`

```py
import email.parser
import socket
from email.parser import Parser
from functools import lru_cache
from urllib.parse import parse_qs, urlparse


class Dairy:
    def __init__(self):
        self.subjects = {}

    def add(self, subject, grade):
        if subject not in self.subjects:
            self.subjects[subject] = []
            self.subjects[subject].append(grade)
        else:
            self.subjects[f"{subject}"].append(grade)

    def mean(self, the_subject):
        if the_subject not in self.subjects or len(self.subjects[the_subject]) == 0:
            return None

        total_sum = sum(self.subjects[the_subject])

        amount = len(self.subjects[the_subject])
        return total_sum / amount


class HTTPError(Exception):
    def __init__(self, the_status, the_reason, the_body=None):
        super().__init__(f"{the_status} {the_reason}")
        self.status = the_status
        self.reason = the_reason
        self.body = the_body

    def __str__(self):
        return f"HTTPError: {self.status} {self.reason}" + (f"\nBody: {self.body}" if self.body else "")


class Request:
    def __init__(self, the_method, the_target, the_version, the_headers, the_rfile):
        self.method = the_method
        self.target = the_target
        self.version = the_version
        self.headers = the_headers
        self.rfile = the_rfile

    @property
    def path(self):
        return self.url.path

    @property
    @lru_cache(maxsize=None)
    def query(self):
        return parse_qs(self.url.query)

    @property
    @lru_cache(maxsize=None)
    def url(self):
        return urlparse(self.target)


class Response:
    def __init__(self, the_status, the_reason, the_headers=None, the_body=None):
        self.status = the_status
        self.reason = the_reason
        self.headers = the_headers
        self.body = the_body


class MyHTTPServer:
    def __init__(self, the_host, the_port, the_name, the_rfile):
        self.host = the_host
        self.port = the_port
        self.name = the_name
        self.rfile = the_rfile
        self.Dairy = Dairy()

    # 1. Запускаю сервер на сокете, обработка входящих соединений
    def serve_forever(self):

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            server_socket.bind((self.host, self.port))
            server_socket.listen(25)
            print("HTTP server is running on", self.host, ':', self.port)
            while True:
                try:
                    client_conn, client_add = server_socket.accept()
                    print('Connection from: ', client_add)
                    self.serve_client(client_conn)
                except Exception as e:
                    print('Client serving failed', e)
        finally:
            server_socket.close()

    # 2. Обработка клиентского подключения
    def serve_client(self, client):
        try:
            request = self.parse_request(client)

            response = self.handle_request(request)
            self.send_response(client, response)
        except Exception as e:
            print(f"Error handling client: {e}")
        finally:
            client.close()

    # 3. функция для обработки заголовка http+запроса. Python, сокет предоставляет возможность создать вокруг
    # него некоторую обертку, которая предоставляет file object интерфейс. Это дайте возможность
    # построчно обработать запрос. Заголовок всегда - первая строка.
    # Первую строку нужно разбить на 3 элемента (метод + url + версия протокола).
    # URL необходимо разбить на адрес и параметры
    # (isu.ifmo.ru/pls/apex/f?p=2143 , где isu.ifmo.ru/pls/apex/f, а p=2143 - параметр p со значением 2143)
    def parse_request(self, client) -> Request:
        headers = []
        max_len = 2048
        file = client.makefile('rb')
        line = file.readline(max_len + 1)

        if len(line) > max_len:
            raise HTTPError(400, 'Bad request', 'Request line is too long')

        de_line = str(line, 'iso-8859-1')
        de_line = de_line.rstrip('\r\n')
        splits = de_line.split()

        if len(splits) != 3:
            print(len(splits))
            raise HTTPError(400, 'Bad request', 'Malformed request line')

        method = splits[0]
        target = splits[1]
        version = splits[2]

        if version != 'HTTP/1.1':
            raise HTTPError(505, 'HTTP Version Not Supported')

        headers = self.parse_headers(file)
        the_host = headers.get('Host')

        if not the_host:
            raise Exception('Bad request')
        if the_host not in (self.host, f'{self.host}:{self.port}'):
            raise Exception('Not found')

        return Request(method, target, version, headers, file)

    # 4. Функция для обработки headers. Необходимо прочитать все заголовки
    # после первой строки до появления пустой строки и сохранить их в массив
    def parse_headers(self, bfile):
        max_len = 2048
        headers = []
        while True:
            line = bfile.readline(max_len + 1)
            if len(line) > max_len:
                raise Exception('Header line is too long')

            if line in (b'\r\n', b'\n', b''):
                break

            headers.append(line)

            if len(headers) > 50:
                raise Exception("Too many headers")

        # Возвращаемое значение метода Parser.parsestr() - это объект email.message.Message, который напоминает
        # OrderedDict. Ключи в Message - это отсортированные в порядке появления ключи заголовков.
        s_headers = b''.join(headers).decode('iso-8859-1')
        return Parser().parsestr(s_headers)

    # Создание записи о новой оценке
    # POST /subjects?name=Web&grade=A HTTP/1.1

    # 5. Функция для обработки url в соответствии с нужным методом. В случае данной работы, нужно будет создать набор
    # условий, который обрабатывает GET или POST запрос. GET запрос должен возвращать данные.
    # POST запрос должен записывать данные на основе переданных параметров.
    def handle_request(self, request):
        if request.path == '/':
            body = self.generate_html()
            return Response(200, 'OK', [('Content-Type', 'text/html; charset=utf-8')], body.encode())
        if request.method == 'GET':
            return self.handle_get_grades(request)
        elif request.method == 'POST':
            return self.handle_post_grades(request)
        raise HTTPError(404, 'Not Found')

    # 6. Функция для отправки ответа. Необходимо записать в соединение status line вида HTTP/1.1 <status_code> <reason>.
    # Затем, построчно записать заголовки и пустую строку, обозначающую конец секции заголовков.
    def send_response(self, conn, resp):
        wfile = conn.makefile('wb')
        try:
            status_line = f'HTTP/1.1 {resp.status} {resp.reason}\r\n'
            wfile.write(status_line.encode('iso-8859-1'))

            if resp.headers:
                for key, value in resp.headers.items() if isinstance(resp.headers, dict) else resp.headers:
                    header_line = f'{key}: {value}\r\n'
                    wfile.write(header_line.encode('iso-8859-1'))

            if resp.body and not any(key.lower() == 'content-length' for key, _ in resp.headers):
                content_length = len(resp.body) if isinstance(resp.body, bytes) else len(resp.body)
                wfile.write(f'Content-Length: {content_length}\r\n'.encode('iso-8859-1'))

            wfile.write(b'\r\n')

            if resp.body:
                if isinstance(resp.body, str):
                    resp.body = resp.body.encode('utf-8')
                wfile.write(resp.body)
        except Exception as e:
            print(f"Error while sending response: {e}")
        finally:
            wfile.flush()
            wfile.close()

    def handle_post_grades(self, request):
        try:
            print("Parsed query:", request.query)
            name = request.query.get('name')[0]
            grade = request.query.get('grade')[0]

            if not name or not grade:
                raise HTTPError(400, 'Bad Request', 'Missing name or grade')

            # try:
            #     grade = int(grade)
            # except ValueError:
            #     raise HTTPError(400, 'Bad Request', 'Grade must be an integer')

            self.Dairy.add(name.lower(), grade)
            body_html = self.generate_html()

            return Response(200, 'OK', [('Content-Type', 'text/html; charset=utf-8')], body_html.encode())

        except Exception as e:
            raise HTTPError(500, 'Internal Server Error', str(e))

    def handle_get_grades(self, request):
        path_parts = request.path.strip('/').split('/')
        if len(path_parts) == 2 and path_parts[0] == 'users':
            subject = path_parts[1]
            grades = self.Dairy.subjects.get(subject.lower())
            if not grades:
                return Response(404, 'Not Found')

            body = '\n'.join(map(str, grades)).encode()
            return Response(200, 'OK', [('Content-Type', 'text/plain')], body)

        raise HTTPError(404, 'Not Found')

    def generate_html(self):
        body = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Grades in Parallel Universe</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f9f3f3;
            color: #333;
            text-align: center;
            padding: 20px;
        }
        h1 {
            color: #d5006d;
            margin-bottom: 20px;
        }
        table {
            width: 60%;
            margin: 0 auto;
            border-collapse: collapse;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,.1);
        }
        th, td {
            padding: 15px;
            border: 1px solid #d5006d;
            text-align: center;
       }
       th {
           background-color: #ff80ab;
           color: white;
       }
       tr:nth-child(even) {
           background-color: #ffebee;
       }
       tr:hover {
           background-color: #f48fb1;
       }
   </style>
</head>
<body>
    <h1>My Grades in Parallel Universe</h1>"""

        body += '<table><thead><tr><th>Subject</th><th>Grade</th></tr></thead><tbody>'

        for subject in self.Dairy.subjects.keys():
            grades_list = ', '.join(self.Dairy.subjects[subject])
            body += f'<tr><td>{subject}</td><td>{grades_list}</td></tr>'

        body += '</tbody></table>'
        body += '</body></html>'
        return body


if __name__ == '__main__':
    host = 'localhost'
    port = 8080
    name = 'the_name'
    rfile = []
    serv = MyHTTPServer(host, port, name, rfile)
    try:
        print('http://localhost:8080')
        serv.serve_forever()
    except KeyboardInterrupt:
        pass
```

`Client's code`
```py 
import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = 'localhost'
PORT = 8080
BUFF_SIZE = 2048

client_socket.connect((HOST, PORT))


def _post(subject='web', grade=4):
        try:
            query_string = f"name={subject.lower()}&grade={grade}"
            client_request = (
                f"POST /subjects?{query_string} HTTP/1.1\r\n"
                f"Host: {HOST}\r\n\r\n"
                #f"\n\n\n"
            )
            client_socket.send(client_request.encode('iso-8859-1'))
            server_response = client_socket.recv(BUFF_SIZE).decode('iso-8859-1')
            client_socket.close()
            print(server_response)
        except Exception as e:
            print(f"Error: {e}")



def _get(subject='web'):
    try:
        headers = (
            f"GET /users/{subject.lower()} HTTP/1.1\r\n"
            f"Host: {HOST}\r\n\r\n"
        )
        client_socket.sendall(headers.encode('iso-8859-1'))
        server_response = client_socket.recv(BUFF_SIZE).decode('iso-8859-1')
        print(server_response)
        client_socket.close()
    except Exception as e:
        print(f"Error: {e}")


if __name__=='__main__':
    opt = input("post or get: ")
    match opt:
        case 'post':
            sub = input("enter the subject: ")
            gr = int(input("enter the grade: "))
            _post(sub, gr)
        case 'get':
            sub = input("enter the subject: ")
            _get(sub)
```