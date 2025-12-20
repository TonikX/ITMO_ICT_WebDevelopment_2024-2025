import socket
from urllib.parse import unquote  # Добавляем импорт для декодирования URL

class MyHTTPServer:
    def __init__(self, host, port, server_name):
        self._host = host
        self._port = port
        self._server_name = server_name
        self.grades = {}  # Хранилище оценок {дисциплина: [оценки]}

    def serve_forever(self):
        # 1. Запуск сервера на сокете, обработка входящих соединений
        serv_sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
            proto=0)

        try:
            serv_sock.bind((self._host, self._port))
            serv_sock.listen()
            print(f"Server started on http://{self._host}:{self._port}")

            while True:
                conn, _ = serv_sock.accept()
                try:
                    self.serve_client(conn)
                except Exception as e:
                    print('Client serving failed', e)
        finally:
            serv_sock.close()

    def serve_client(self, conn):
        # 2. Обработка клиентского подключения
        try:
            req = self.parse_request(conn)
            resp = self.handle_request(req)
            self.send_response(conn, resp)
        except ConnectionResetError:
            conn = None
        except Exception as e:
            self.send_error(conn, e)

    def parse_request(self, conn):
        # 3. Обработка заголовка HTTP запроса
        rfile = conn.makefile('rb')  # Создаем file object для чтения
        method, target, version = self.parse_request_line(rfile)
        headers = self.parse_headers(rfile)

        # Читаем тело запроса для POST
        body = b''
        if method == 'POST':
            content_length = int(headers.get('Content-Length', 0))
            if content_length > 0:
                body = rfile.read(content_length)

        rfile.close()
        return {
            'method': method,
            'target': target,
            'version': version,
            'headers': headers,
            'body': body.decode('utf-8')
        }

    def parse_request_line(self, rfile):
        # Парсим первую строку запроса
        line = rfile.readline().decode('utf-8').strip()
        parts = line.split(' ')
        if len(parts) != 3:
            raise Exception("Invalid request line")
        return parts[0], parts[1], parts[2]

    def parse_headers(self, rfile):
        # 4. Обработка headers (читаем до пустой строки)
        headers = {}
        while True:
            line = rfile.readline().decode('utf-8').strip()
            if not line:  # Пустая строка - конец заголовков
                break
            if ':' in line:
                key, value = line.split(':', 1)
                headers[key.strip()] = value.strip()
        return headers

    def handle_request(self, req):
        # 5. Обработка URL в соответствии с методом
        method = req['method']
        target = req['target']

        if method == 'GET' and target == '/':
            return self.handle_get()
        elif method == 'POST' and target == '/add':
            return self.handle_post(req['body'])
        else:
            raise Exception("404 Not Found")

    def handle_get(self):
        # Генерируем HTML страницу с оценками
        html = f"""
        <html>
        <head><title>Оценки - {self._server_name}</title></head>
        <body>
            <h1>Список оценок</h1>
        """

        if self.grades:
            for subject, marks in self.grades.items():
                html += f"<h2>{subject}: {', '.join(marks)}</h2>"
        else:
            html += "<p>Оценок пока нет</p>"

        html += """
            <h3>Добавить оценку</h3>
            <form method="POST" action="/add">
                Дисциплина: <input type="text" name="subject"><br>
                Оценка: <input type="number" name="grade"><br>
                <input type="submit" value="Добавить">
            </form>
            </body></html>
        """

        return {
            'status': 200,
            'reason': 'OK',
            'headers': {'Content-Type': 'text/html; charset=utf-8'},
            'body': html
        }

    def handle_post(self, body):
        # Обрабатываем POST данные (формат: subject=математика&grade=5)
        params = {}
        for pair in body.split('&'):
            if '=' in pair:
                key, value = pair.split('=')
                params[key] = unquote(value)

        subject = params.get('subject', '')
        grade = params.get('grade', '')

        if subject and grade:
            if subject in self.grades:
                self.grades[subject].append(grade)
            else:
                self.grades[subject] = [grade]
            print(f"Added grade: {subject} - {grade}")

        # Перенаправляем на главную страницу
        return {
            'status': 303,
            'reason': 'See Other',
            'headers': {'Location': '/'},
            'body': ''
        }

    def send_response(self, conn, resp):
        # 6. Отправка ответа
        wfile = conn.makefile('wb')  # File object для записи

        # Status line
        status_line = f"HTTP/1.1 {resp['status']} {resp['reason']}\r\n"
        wfile.write(status_line.encode('utf-8'))

        # Headers
        for key, value in resp['headers'].items():
            header_line = f"{key}: {value}\r\n"
            wfile.write(header_line.encode('utf-8'))

        # Empty line
        wfile.write(b"\r\n")

        # Body
        if resp['body']:
            wfile.write(resp['body'].encode('utf-8'))

        wfile.flush()
        wfile.close()
        conn.close()

    def send_error(self, conn, err):
        # Отправка ошибки
        error_html = f"""
        <html><body>
            <h1>Error</h1>
            <p>{str(err)}</p>
        </body></html>
        """

        response = {
            'status': 500,
            'reason': 'Internal Server Error',
            'headers': {'Content-Type': 'text/html; charset=utf-8'},
            'body': error_html
        }

        self.send_response(conn, response)


if __name__ == '__main__':
    host = 'localhost'
    port = 8888
    name = 'Grade Server'

    serv = MyHTTPServer(host, port, name)
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped")