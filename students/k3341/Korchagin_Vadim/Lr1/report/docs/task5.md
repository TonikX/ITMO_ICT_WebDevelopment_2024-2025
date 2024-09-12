# Реализация простого веб-сервера для обработки GET и POST HTTP-запросов

## Условие

**Задача**: Написать простой веб-сервер для обработки GET и POST HTTP-запросов с помощью библиотеки `socket` в Python. Сервер должен выполнять следующие функции:
1. Принимать и записывать информацию о дисциплине и оценке по дисциплине.
2. Отдавать информацию обо всех оценках по дисциплинам в виде HTML-страницы.

##  Решение

В рамках задания был реализован простой веб-сервер, который обрабатывает запросы и управляет информацией о дисциплинах и оценках. Основные функции сервера включают добавление новых дисциплин и оценок, а также предоставление информации о всех оценках в виде HTML-страницы и JSON формате.

### Основные классы

1. **Класс `MyHTTPServer`**: Основной класс, реализующий работу веб-сервера. Он управляет подключениями клиентов, обрабатывает запросы и отправляет ответы.

2. **Класс `Request`**: Представляет HTTP-запрос и предоставляет методы для доступа к методу запроса, пути, заголовкам и параметрам запроса.

3. **Класс `Response`**: Представляет HTTP-ответ, который сервер отправляет клиенту. Содержит статус, описание, заголовки и тело ответа.

4. **Класс `HTTPError`**: Используется для представления ошибок HTTP и формирования соответствующих ответов с ошибками.

### Основные функции

1. **`serve_forever`**:
> Запускает сервер, который ожидает подключения клиентов.
> Принимает клиентские подключения и передает их для обработки в метод `serve_client`.

2. **`serve_client`**:
> Обрабатывает запрос клиента, включая разбор запроса, обработку и отправку ответа.
> В случае ошибки отправляет соответствующий ответ об ошибке.

3. **`parse_request`**:
> Разбирает запрос клиента, извлекая метод, путь, версию HTTP и заголовки.
> Проверяет корректность заголовка `Host`.

4. **`handle_request`**:
> Определяет тип запроса (POST или GET) и передает его в соответствующую функцию для обработки:
> `handle_post_subject` для добавления новой дисциплины.
> `handle_get_subjects` для получения списка дисциплин.
> `handle_get_marks` для получения оценок по дисциплине. 
> `handle_add_mark` для добавления оценки по дисциплине.

5. **`handle_post_subject`**:
> Добавляет новую дисциплину в базу данных сервера.
> Дисциплина идентифицируется по уникальному ID и хранится вместе с пустым списком оценок.

6. **`handle_get_subjects`**:
> Возвращает список всех дисциплин в зависимости от типа запрашиваемого контента (`text/html` или `application/json`).
> Если запрашивается HTML, генерируется HTML-страница со списком дисциплин или JSON.

7. **`handle_get_marks`**:
> Возвращает оценки по заданной дисциплине в формате HTML или JSON.
> Генерирует HTML-страницу, если запрашивается HTML, или возвращает JSON-данные.

8. **`handle_add_mark`**:
> Добавляет оценку к заданной дисциплине.
> Проверяет корректность значения оценки (должна быть в диапазоне от 0 до 100).

9. **`send_response`**:
> Отправляет HTTP-ответ клиенту.
> Формирует статусную строку, заголовки и тело ответа.

10. **`send_error`**:
> Отправляет ответ об ошибке в случае возникновения исключений.

### Пример работы

1. **Добавление новой дисциплины**:
> Клиент отправляет POST-запрос на `/subjects` с параметрами `name` (название дисциплины). 
> Сервер добавляет дисциплину и возвращает ответ.
2. **Получение списка дисциплин**:
>Клиент отправляет GET-запрос на `/subjects`.
>Сервер возвращает список дисциплин в виде HTML или JSON в зависимости от заголовка `Accept`.
3. **Добавление оценки по дисциплине**:
> Клиент отправляет POST-запрос на `/subjects/{subject_id}` с параметром `mark` (оценка).
> Сервер добавляет оценку и возвращает ответ.
4. **Получение оценок по дисциплине**:    
> Клиент отправляет GET-запрос на `/subjects/{subject_id}`.
> Сервер возвращает оценки в формате HTML или JSON в зависимости от заголовка `Accept`.

## Код

```python
import socket
import json
from email.parser import Parser
from urllib.parse import parse_qs, urlparse
from functools import lru_cache

MAX_LINE = 64 * 1024
MAX_HEADERS = 100

class MyHTTPServer:
    def __init__(self, host, port, server_name):
        self._host = host
        self._port = port
        self._server_name = server_name
        self._subjects = {}

    def serve_forever(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
        try:
            server_socket.bind((self._host, self._port))
            server_socket.listen()
            while True:
                client_socket, _ = server_socket.accept()
                try:
                    self.serve_client(client_socket)
                except Exception as e:
                    print('Client serving failed:', e)
        finally:
            server_socket.close()

    def serve_client(self, client_socket):
        try:
            request = self.parse_request(client_socket)
            response = self.handle_request(request)
            self.send_response(client_socket, response)
        except ConnectionResetError:
            client_socket = None
        except Exception as e:
            self.send_error(client_socket, e)

        if client_socket:
            client_socket.close()

    def parse_request(self, client_socket):
        rfile = client_socket.makefile('rb')
        method, target, version = self.parse_request_line(rfile)
        headers = self.parse_headers(rfile)

        host = headers.get('Host')
        if not host:
            raise HTTPError(400, 'Bad request', 'Host header is missing')
        if host not in (self._server_name, f'{self._server_name}:{self._port}'):
            raise HTTPError(404, 'Not found')

        print(method, target, version, headers)
        return Request(method, target, version, headers, rfile)

    def parse_request_line(self, file):
        line = file.readline(MAX_LINE + 1)
        if len(line) > MAX_LINE:
            raise HTTPError(400, 'Bad request', 'Request line is too long')

        req_line = str(line, "iso-8859-1")
        req_line = req_line.rstrip("\r\n")
        words = req_line.split()
        if len(words) != 3:
            raise HTTPError(400, 'Bad request', 'Malformed request line')

        method, target, version = words
        if version != "HTTP/1.1":
            raise HTTPError(505, 'HTTP Version Not Supported')

        return method, target, version

    def parse_headers(self, file):
        headers = []
        while True:
            line = file.readline(MAX_LINE + 1)
            if len(line) > MAX_LINE:
                raise HTTPError(494, 'Request header too large')
            if line in (b"\r\n", b"\n", b""):
                break
            headers.append(line)
            if len(headers) > MAX_HEADERS:
                raise HTTPError(494, 'Too many headers')

        sheaders = b"".join(headers).decode('iso-8859-1')
        return Parser().parsestr(sheaders)

    def handle_request(self, req):
        if req.path == '/subjects' and req.method == 'POST':
            return self.handle_post_subject(req)

        if req.path == '/subjects' and req.method == 'GET':
            return self.handle_get_subjects(req)

        if req.path.startswith('/subjects/'):
            subject_id = req.path[len('/subjects/'):]
            if req.method == 'GET':
                return self.handle_get_marks(req, subject_id)
            if req.method == 'POST':
                return self.handle_add_mark(req, subject_id)

        raise HTTPError(404, 'Not found')

    def handle_post_subject(self, req):
        subject_id = len(self._subjects) + 1
        self._subjects[subject_id] = {
            'id': subject_id,
            'name': req.query['name'][0],
            'mark': [],
        }
        return Response(204, 'Created')

    def handle_get_subjects(self, req):
        accept = req.headers.get('Accept')

        if 'text/html' in accept:
            content_type = 'text/html; charset=utf-8'
            body = self._generate_html_subjects_body()
        elif 'application/json' in accept:
            content_type = 'application/json; charset=utf-8'
            body = json.dumps(list(self._subjects.values())).encode('utf-8')
        else:
            return Response(406, 'Not Acceptable')

        headers = [
            ('Content-Type', content_type),
            ('Content-Length', str(len(body)))
        ]
        return Response(200, 'OK', headers, body)

    def _generate_html_subjects_body(self):
        subjects_list = ''.join(
            f'<li>{subj["id"]}: {subj["name"]}</li>'
            for subj in self._subjects.values()
        )
        html = f'''
        <html>
          <head><title>Subjects</title></head>
          <body>
            <ul>{subjects_list}</ul>
          </body>
        </html>
        '''
        return html.strip().encode('utf-8')
    def handle_get_marks(self, req, subject_id):
        try:
            subject_id = int(subject_id)
            subject = self._subjects.get(subject_id)
            if not subject:
                raise HTTPError(404, 'Subject not found')

            accept = req.headers.get('Accept', '')
            if 'text/html' in accept:
                content_type = 'text/html; charset=utf-8'
                body = self._generate_html_marks_body(subject)
            elif 'application/json' in accept:
                content_type = 'application/json; charset=utf-8'
                body = json.dumps(subject).encode('utf-8')
            else:
                return Response(406, 'Not Acceptable')

            headers = [
                ('Content-Type', content_type),
                ('Content-Length', str(len(body)))
            ]
            return Response(200, 'OK', headers, body)
        except ValueError:
            raise HTTPError(400, 'Invalid subject ID')

    def _generate_html_marks_body(self, subject):
        marks_list = ''.join(f'<li>{mark}</li>' for mark in subject['mark'])
        html = f'''
        <html>
          <head><title>Marks for {subject["name"]}</title></head>
          <body>
            <h1>Marks for {subject["name"]}</h1>
            <ul>{marks_list}</ul>
          </body>
        </html>
        '''
        return html.strip().encode('utf-8')

    def handle_add_mark(self, req, subject_id):
        try:
            subject_id = int(subject_id)
            subject = self._subjects.get(subject_id)
            if not subject:
                raise HTTPError(404, 'Subject not found')

            if 'mark' not in req.query:
                raise HTTPError(400, 'Mark is required')

            mark = req.query['mark'][0]
            try:
                mark = float(mark)
                if not (0 <= mark <= 100):
                    raise ValueError
            except ValueError:
                raise HTTPError(400, 'Invalid mark value')

            subject['mark'].append(mark)

            return Response(204, 'Mark added')
        except ValueError:
            raise HTTPError(400, 'Invalid subject ID')
    def send_response(self, conn, resp):
        wfile = conn.makefile('wb')
        status_line = f'HTTP/1.1 {resp.status} {resp.reason}\r\n'
        wfile.write(status_line.encode('iso-8859-1'))

        if resp.headers:
            for key, value in resp.headers:
                header_line = f"{key}: {value}\r\n"
                wfile.write(header_line.encode("iso-8859-1"))

        wfile.write(b"\r\n")
        if resp.body:
            wfile.write(resp.body)

        wfile.flush()
        wfile.close()

    def send_error(self, conn, err):
        try:
            status = err.status
            reason = err.reason
            body = (err.body or err.reason).encode('utf-8')
        except:
            status = 500
            reason = 'Internal Server Error'
            body = 'Internal Server Error'.encode('utf-8')

        resp = Response(status, reason, [('Content-Length', len(body))], body)
        self.send_response(conn, resp)


class Request:
    def __init__(self, method, target, version, headers, rfile):
        self.method = method
        self.target = target
        self.version = version
        self.headers = headers
        self.rfile = rfile

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
    def __init__(self, status, reason, headers=None, body=None):
        self.status = status
        self.reason = reason
        self.headers = headers
        self.body = body


class HTTPError(Exception):
    def __init__(self, status, reason, body=None):
        super().__init__()
        self.status = status
        self.reason = reason
        self.body = body


if __name__ == '__main__':
    host = '127.0.0.1'
    port = 12345
    server_name = 'example.local'
    server = MyHTTPServer(host, port, server_name)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
```
