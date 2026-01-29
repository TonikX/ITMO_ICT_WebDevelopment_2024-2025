import socket
from dataclasses import dataclass
from email.parser import Parser
from urllib.parse import parse_qs, urlparse, unquote_plus


HOST = 'localhost'
PORT = 8080
NAME = 'MyServer'

MAX_LINE = 64*1024
MAX_HEADERS = 100


@dataclass
class Request:
    method: str
    target: str
    version: str
    headers: dict
    body: str

    @property
    def url(self):
        return urlparse(self.target)
    
    @property
    def path(self):
        return self.url.path
    
    @property
    def query(self):
        return parse_qs(self.url.query)


class MyHTTPServer:
    def __init__(self, host, port, server_name):
        self._host = host
        self._port = port
        self._server_name = server_name
        self.grades = {}


    def serve_forever(self):
        serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            serv_sock.bind((self._host, self._port))
            serv_sock.listen()
            print(f"[СЕРВЕР] Запущен на http://{self._host}:{self._port}")

            while True:
                conn, addr = serv_sock.accept()
                print(f"[СЕРВЕР] Подключение от {addr}")

                try:
                    self.serve_client(conn)
                except Exception as e:
                    print('Client serving failed', e)
        
        except KeyboardInterrupt:
            print("\n[СЕРВЕР] Остановка сервера...")

        finally:
            serv_sock.close()


    def serve_client(self, conn):
        try:
            req = self.parse_request(conn)
            resp = self.handle_request(req)
            self.send_response(conn, resp)
        
        except ConnectionResetError:
            conn = None
        
        except Exception as e:
            self.send_error(conn, e)

        if conn:
            conn.close()


    def parse_request(self, conn):
        rfile = conn.makefile('rb')
        
        method, target, version = self.parse_request_line(rfile)
        headers = self.parse_headers(rfile)
        
        body = ''
        if method == 'POST':
            content_length = int(headers.get('Content-Length', 0))
            if content_length > 0:
                body = rfile.read(content_length).decode('utf-8')
        
        host = headers.get('Host')
        
        if not host:
            raise Exception("Bad request")
        
        # Проверяем на реальный хост, а не на имя сервера
        if host not in (
            f"{self._host}:{self._port}",
            self._host
        ):
            raise Exception("Not found")
        
        return Request(method, target, version, headers, body)


    def parse_request_line(self, rfile):
        raw = rfile.readline(MAX_LINE + 1)
        
        if len(raw) > MAX_LINE:
            raise Exception("Request line is too long")
        
        req_line = str(raw, 'iso-8859-1').rstrip('\r\n')
        words = req_line.split(' ')

        if len(words) != 3:
            raise Exception("Request line is malformed")
        
        method, target, version = words

        if method not in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']:
            raise Exception("Unknown HTTP method")
        
        if version != 'HTTP/1.1':
            raise Exception("Unknown HTTP version")
        
        return method, target, version
    

    def parse_headers(self, rfile):
        headers = []

        while True:
            line = rfile.readline(MAX_LINE + 1)
            
            if len(line) > MAX_LINE:
                raise Exception("Header line is too long")
            
            if line in (b'\r\n', b'\n', b''):
                break
            
            headers.append(line)
        
        if len(headers) > MAX_HEADERS:
            raise Exception('Too many headers')
        
        sheaders = b''.join(headers).decode('iso-8859-1')
        return Parser().parsestr(sheaders)
    

    def handle_request(self, req):
        if req.path == '/grades' and req.method == 'GET':
            return self.handle_get_grades(req)
        elif req.path == '/grades' and req.method == 'POST':
            return self.handle_post_grades(req)
        elif req.path == '/grades/add' and req.method == 'GET':
            return self.handle_get_form(req)
        else:
            raise Exception("Not found")


    def handle_get_grades(self, req):
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Все оценки</title>
            <style>
                body { font-family: Arial; max-width: 900px; margin: 50px auto; padding: 20px; }
                h1 { color: #333; }
                table { width: 100%; border-collapse: collapse; margin: 20px 0; }
                th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
                th { background: #4CAF50; color: white; }
                tr:hover { background: #f5f5f5; }
                .empty { text-align: center; padding: 40px; color: #999; font-style: italic; }
                a { color: #2196F3; text-decoration: none; margin-top: 20px; display: inline-block; }
                a:hover { text-decoration: underline; }
                .grades-list { display: flex; gap: 5px; flex-wrap: wrap; align-items: center; }
                .grade-badge { background: #e3f2fd; padding: 4px 8px; border-radius: 4px; font-weight: bold; color: #1976d2; }
            </style>
        </head>
        <body>
            <h1>Все оценки по дисциплинам</h1>
        """

        if self.grades:
            html += """
            <table>
                <tr>
                    <th>Дисциплина</th>
                    <th>Оценки</th>
                </tr>
            """
        
            for subj, grades_list in self.grades.items():
                grades_html = '<div class="grades-list">'
                for grade in grades_list:
                    grades_html += f'<span class="grade-badge">{grade}</span>'
                grades_html += '</div>'
                                
                html += f"""
                <tr>
                    <td>{subj}</td>
                    <td>{grades_html}</td>
                </tr>
                """
            
            html += "</table>"

        else:
            html += '<div class="empty">Оценок пока нет. Добавьте первую!</div>'
        
        html += """
            <a href="/grades/add">← Добавить новую оценку</a>
        </body>
        </html>
        """

        return html.encode('utf-8')


    def handle_post_grades(self, req):
        data = parse_qs(req.body)

        subject = data.get('subject', [''])[0]
        grade = data.get('grade', [''])[0]

        if not subject or not grade:
            raise Exception("Bad request: missing fields")
        
        subject = unquote_plus(subject)
        grade = unquote_plus(grade)
        
        if subject not in self.grades:
            self.grades[subject] = []
        
        self.grades[subject].append(grade)

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Оценка добавлена</title>
            <style>
                body {{ font-family: Arial; max-width: 600px; margin: 50px auto; padding: 20px; text-align: center; }}
                .success {{ background: #d4edda; border: 1px solid #c3e6cb; color: #155724; padding: 20px; border-radius: 8px; margin: 20px 0; }}
                h1 {{ color: #155724; }}
                .info {{ background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 20px 0; }}
                a {{ display: inline-block; margin: 10px; padding: 10px 20px; color: white; text-decoration: none; border-radius: 4px; }}
                .btn-primary {{ background: #4CAF50; }}
                .btn-secondary {{ background: #2196F3; }}
                a:hover {{ opacity: 0.8; }}
            </style>
        </head>
        <body>
            <div class="success">
                <h1>✓ Оценка успешно добавлена!</h1>
            </div>
            <div class="info">
                <p><strong>Дисциплина:</strong> {subject}</p>
                <p><strong>Оценка:</strong> {grade}</p>
            </div>
            <a href="/grades/add" class="btn-primary">Добавить еще одну</a>
            <a href="/grades" class="btn-secondary">Посмотреть все оценки</a>
        </body>
        </html>
        """
    
        return html.encode('utf-8')


    def handle_get_form(self, req):
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Добавить оценку</title>
            <style>
                body { font-family: Arial; max-width: 600px; margin: 50px auto; padding: 20px; }
                h1 { color: #333; }
                form { background: #f4f4f4; padding: 20px; border-radius: 8px; }
                label { display: block; margin: 10px 0 5px; font-weight: bold; }
                input, select { width: 100%; padding: 8px; margin-bottom: 15px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }
                button { background: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; width: 100%; }
                button:hover { background: #45a049; }
                a { display: inline-block; margin-top: 15px; color: #2196F3; text-decoration: none; }
                a:hover { text-decoration: underline; }
            </style>
        </head>
        <body>
            <h1>Добавить оценку по дисциплине</h1>
            <form method="POST" action="/grades">
                <label for="subject">Название дисциплины:</label>
                <input type="text" id="subject" name="subject" required>
                
                <label for="grade">Оценка:</label>
                <select id="grade" name="grade" required>
                    <option value="">Выберите оценку</option>
                    <option value="5">5 (Отлично)</option>
                    <option value="4">4 (Хорошо)</option>
                    <option value="3">3 (Удовлетворительно)</option>
                    <option value="2">2 (Неудовлетворительно)</option>
                </select>
                
                <button type="submit">Добавить оценку</button>
            </form>
            <a href="/grades">Посмотреть все оценки</a>
        </body>
        </html>
        """
        
        return html.encode('utf-8')


    def send_response(self, conn, resp):
        wfile = conn.makefile('wb')

        status_line = "HTTP/1.1 200 OK\r\n"
        wfile.write(status_line.encode('iso-8859-1'))

        headers = [
            f'Server: {self._server_name}\r\n',
            'Content-Type: text/html; charset=utf-8\r\n',
            f'Content-Length: {len(resp)}\r\n',
            'Connection: close\r\n',
            '\r\n'
        ]

        for header in headers:
            wfile.write(header.encode('iso-8859-1'))
    
        wfile.write(resp)
        wfile.flush()


    def send_error(self, conn, err):
        try:
            wfile = conn.makefile('wb')
            
            status = '404 Not Found'
            body = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>Ошибка</title>
                <style>
                    body {{ font-family: Arial; text-align: center; padding: 50px; }}
                    h1 {{ color: #d32f2f; }}
                    p {{ color: #666; }}
                    a {{ color: #2196F3; text-decoration: none; }}
                </style>
            </head>
            <body>
                <h1>Ошибка</h1>
                <p>{err}</p>
                <a href="/grades/add">← Вернуться на главную</a>
            </body>
            </html>
            """.encode('utf-8')
            
            status_line = f'HTTP/1.1 {status}\r\n'
            wfile.write(status_line.encode('iso-8859-1'))
            
            headers = [
                f'Server: {self._server_name}\r\n',
                'Content-Type: text/html; charset=utf-8\r\n',
                f'Content-Length: {len(body)}\r\n',
                'Connection: close\r\n',
                '\r\n'
            ]
            
            for header in headers:
                wfile.write(header.encode('iso-8859-1'))
            
            wfile.write(body)
            wfile.flush()
            
        except Exception as e:
            print(f'Failed to send error: {e}')


if __name__ == '__main__':
    serv = MyHTTPServer(HOST, PORT, NAME)
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        pass