# Отчет
## Задание 1
Реализовать клиентскую и серверную часть приложения. Клиент отправляет серверу сообщение «Hello, server», и оно должно отобразиться на стороне сервера. В ответ сервер отправляет клиенту сообщение «Hello, client», которое должно отобразиться у клиента.

Требования:

    Обязательно использовать библиотеку socket.
    Реализовать с помощью протокола UDP.

Реализация сервера:

    import socket
    
    def server():
        server_address = ('localhost', 8080)
    
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
        sock.bind(server_address)
    
        print("Сервер запущен. Ожидание сообщения от клиента...")
    
        while True:
            data, client_address = sock.recvfrom(4096)
            print(f"Получено сообщение от клиента: {data.decode()}")
    
            message = "Hello, client"
            sock.sendto(message.encode(), client_address)
            print(f"Отправлено сообщение клиенту: {message}")
    
    
    if __name__ == "__main__":
        server()

Реализация клиента:

    import socket
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    client_socket.connect(('localhost', 8080))
    
    client_socket.sendall(b'Hello, server')
    
    response = client_socket.recv(1024)
    print(f'Ответ от сервера: {response.decode()}')
    
    client_socket.close()

## Задание 2
Реализовать клиентскую и серверную часть приложения. Клиент запрашивает выполнение математической операции, параметры которой вводятся с клавиатуры. Сервер обрабатывает данные и возвращает результат клиенту.

Варианты операций:

    Теорема Пифагора.
    Решение квадратного уравнения.
    Поиск площади трапеции.
    Поиск площади параллелограмма.

Порядок выбора варианта: Выбирается по порядковому номеру в журнале (пятый студент получает вариант 1 и т.д.).

Требования:

    Обязательно использовать библиотеку socket.
    Реализовать с помощью протокола TCP.

Реализация сервера:

    import socket
    
    def solve_quadratic_equation(a, b, c):
        discriminant = b**2 - 4*a*c
        if discriminant < 0:
            return None
        elif discriminant == 0:
            x = -b / (2*a)
            return (x, x)
        else:
            x1 = (-b + (discriminant)**0.5) / (2*a)
            x2 = (-b - (discriminant)**0.5) / (2*a)
            return (x1, x2)
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    server_socket.bind(('localhost', 8080))
    
    server_socket.listen(1)
    print("Сервер запущен на порту 8080...")
    
    while True:
        client_connection, client_address = server_socket.accept()
        print(f'Подключение от {client_address}')
    
        request = client_connection.recv(1024).decode()
        a, b, c = request.split()
        solution = solve_quadratic_equation(float(a),  float(b), float(c))
        if solution is None:
            response = 'Корней нет'
        elif solution[0] == solution[1]:
            response = f'Корень уравнения: {solution[0]}'
        else:
            response = f'Корни уравнения: {solution[0]} и {solution[1]}'
        client_connection.sendall(response.encode())
    
        client_connection.close()

Реализация клиента:

    import socket
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    client_socket.connect(('localhost', 8080))
    
    a = float(input("Введите коэффициент a: "))
    b = float(input("Введите коэффициент b: "))
    c = float(input("Введите коэффициент c: "))
    params = str(a) + " " + str(b) + " " + str(c)
    
    client_socket.sendall(params.encode())
    
    data = client_socket.recv(1024).decode()
    print(f"Ответ сервера: {data}")
    
    client_socket.close()

## Задание 3
Реализовать серверную часть приложения. Клиент подключается к серверу, и в ответ получает HTTP-сообщение, содержащее HTML-страницу, которая сервер подгружает из файла index.html.

Требования:

    Обязательно использовать библиотеку socket.

Реализация сервера:

    import socket
    
    host = 'localhost'
    port = 8080
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    server_socket.bind((host, port))
    
    server_socket.listen(5)
    print(f"HTTP-сервер запущен на {host}:{port}")
    
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Новое подключение от {client_address}")
    
        with open("index.html", "r", encoding="utf-8") as file:
            html_content = file.read()
    
        response = (
            "HTTP/1.1 200 OK\n"
            "Content-Type: text/html; charset=utf-8\n"
            "Content-Length: {}\n\n{}".format(len(html_content.encode("utf-8")), html_content)
        )
    
        client_socket.sendall(response.encode())
    
        client_socket.close()

HTML код:

    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>Реквест - респонс</title>
    </head>
    <body>
        <h1>Реквест - респонс</h1>
        <p>
        <a href="https://www.youtube.com/watch?v=DjVB2P15iUo" target="_blank">
            Кликать сюда
        </a>
    </p>
        <p>
            Будь то Рыбацкое или Южный Бронкс,<br>
            Если есть реквест, то я найду респонс.<br>
            Реквест - респонс.<br>
            Реквест, реквест - респонс, респонс.<br>
        </p>
        <p>
            100 означает: "Обожди, фраерок".<br>
            Если я ответил 200, значит, всё ОК.<br>
            Если в деле братва, но надо мозговать сперва -<br>
            Качаем головами, отвечаем 202.<br>
            302, если брат без тормозов<br>
            Был временно перемещён в СИЗО.<br>
            301 - баба плачь, малой, пришли открытку -<br>
            Батяня постоянно перемещён на крытку.<br>
        </p>
        <p>
            Будь то Рыбацкое или Южный Бронкс,<br>
            Если есть реквест, то я найду респонс.<br>
            Реквест - респонс.<br>
            Реквест, реквест - респонс, респонс. x2<br>
        </p>
        <p>
            Эй? ты! Кто ты? Чё смотришь, пёс?<br>
            400 - не по понятиям запрос.<br>
            401 - таков мой ответ<br>
            Тем, кто не знает, где спрашивать, где нет.<br>
            403 говорит о том,<br>
            Что я не стану вести бесед с ментом.<br>
            Хозяева не нашли вещей в своей квартире?<br>
            А мы-то тут при чём? 404!<br>
        </p>
        <p>
            Будь то Рыбацкое или Южный Бронкс,<br>
            Если есть реквест, то я найду респонс.<br>
            Реквест - респонс.<br>
            Реквест, реквест - респонс, респонс. x2<br>
        </p>
        <p>
            Если перекрыт, то "200 ОК" не говори.<br>
            Отвечай 500, 501, 503. x4<br>
        </p>
        <p>
            Будь то Рыбацкое или Южный Бронкс,<br>
            Если есть реквест, то я найду респонс.<br>
            Реквест - респонс.<br>
            Реквест, реквест - респонс, респонс. x2<br>
        </p>
        <p>
            Будь то Рыбацкое или Южный Бронкс,<br>
            Если есть реквест, то я найду респонс. x2<br>
        </p>
    </body>
    </html>


## Задание 4
Реализовать двухпользовательский или многопользовательский чат. Для максимального количества баллов реализуйте многопользовательский чат.

Требования:

    Обязательно использовать библиотеку socket.
    Для многопользовательского чата необходимо использовать библиотеку threading.

Реализация:

    Протокол TCP: 100% баллов.
    Протокол UDP: 80% баллов.
    Для UDP используйте threading для получения сообщений на клиенте.
    Для TCP запустите клиентские подключения и обработку сообщений от всех пользователей в потоках. Не забудьте сохранять пользователей, чтобы отправлять им сообщения.

Реализация сервера:

    import socket
    import threading
    
    clients = {}
    
    def broadcast(message, sender_socket=None):
        for client, name in clients.items():
            if client != sender_socket:
                    client.send(message.encode('utf-8'))
    
    
    def handle_client(client_socket):
        client_socket.send("Введите своё имя: ".encode('utf-8'))
        client_name = client_socket.recv(1024).decode('utf-8').strip()
        clients[client_socket] = client_name
        print(f"{client_name} подключился.")
    
        broadcast(f"{client_name} присоединился к чату!", sender_socket=client_socket)
    
        while True:
            message = client_socket.recv(1024).decode('utf-8').strip()
            if not message:
                break
            print(f"{client_name}: {message}")
            broadcast(f"{client_name}: {message}", sender_socket=client_socket)
    
    
    def start_server(host='127.0.0.1', port=5555):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"Сервер запущен на {host}:{port}")
    
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Новое подключение: {client_address}")
    
            threading.Thread(target=handle_client, args=(client_socket,), daemon=True).start()
    
    
    if __name__ == "__main__":
        start_server()

Реализация клиента:

import socket
import threading


    def receive_messages(client_socket):
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(message)
    
    
    def send_messages(client_socket):
        while True:
            message = input()
            client_socket.send(message.encode('utf-8'))
    
    
    def start_client(host='127.0.0.1', port=5555):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
    
        print("Подключено к серверу.")
    
        threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()
    
        name = input("Введите своё имя: ")
        client_socket.send(name.encode('utf-8'))
    
        send_messages(client_socket)
    
    if __name__ == "__main__":
        start_client()


## Задание 5
Написать простой веб-сервер для обработки GET и POST HTTP-запросов с помощью библиотеки socket в Python.

Задание:

    Сервер должен:
        Принять и записать информацию о дисциплине и оценке по дисциплине.
        Отдать информацию обо всех оценках по дисциплинам в виде HTML-страницы.

Реализация сервера:

    import socket
    
    MAX_LINE = 64 * 1024
    
    class MyHTTPServer:
        def __init__(self, host='localhost', port=8081):
            self.host = host
            self.port = port
            self._subjects = {}
    
        def serve_forever(self):
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.bind((self.host, self.port))
            server.listen()
            print(f'Server started on http://{self.host}:{self.port}')
            while True:
                conn, _ = server.accept()
                self.serve_client(conn)
    
        def serve_client(self, conn):
            try:
                req = self.parse_request(conn)
                resp = self.handle_request(req)
                self.send_response(conn, resp)
            except Exception as e:
                self.send_error(conn, e)
            finally:
                conn.close()
    
        def parse_request(self, conn):
            rfile = conn.makefile('rb')
            method, target, _ = self.parse_request_line(rfile)
            headers = self.parse_headers(rfile)
            return Request(method, target, headers, rfile)
    
        def parse_request_line(self, rfile):
            raw = rfile.readline(MAX_LINE + 1)
            if len(raw) > MAX_LINE:
                raise ValueError('Request line too long')
            req_line = str(raw, 'iso-8859-1').strip()
            method, target, version = req_line.split()
            if version != 'HTTP/1.1':
                raise ValueError('HTTP version not supported')
            return method, target, version
    
        def parse_headers(self, rfile):
            headers = {}
            while True:
                line = rfile.readline(MAX_LINE + 1)
                if not line or line in (b"\r\n", b"\n"):
                    break
                header = str(line, 'iso-8859-1').strip()
                key, value = header.split(': ', 1)
                headers[key] = value
            return headers
    
        def handle_request(self, req):
            if req.method == 'GET':
                if req.path == '/':
                    return self.handle_get_subjects()
                elif req.path.startswith('/subject/'):
                    subject_id = req.path[len('/subject/'):]
                    return self.handle_get_subject_by_id(subject_id)
            elif req.method == 'POST' and req.path == '/subject':
                return self.handle_post_subject(req)
            else:
                raise ValueError('Unsupported method')
    
        def handle_post_subject(self, req):
            content_length = int(req.headers.get('Content-Length', 0))
            body = req.rfile.read(content_length).decode('iso-8859-1')
            params = dict(param.split('=') for param in body.split('&'))
    
            if "name" not in params or 'mark' not in params:
                raise ValueError('The name and mark parameters are required')
    
            name = params.get('name')
            mark = params.get('mark')
    
            # Поиск предмета по имени
            subject = next((s for s in self._subjects.values() if s['name'] == name), None)
    
            if subject:
                # Если предмет существует, добавляем новую оценку
                subject['marks'].append(mark)
            else:
                # Если предмет не найден, создаём новый
                sub_id = len(self._subjects) + 1
                self._subjects[sub_id] = {
                    "id": sub_id,
                    "name": name,
                    "marks": [mark]
                }
    
            return Response(201, "Created")
    
        def handle_get_subjects(self):
            html = """
            <html>
                <head>
                    <title>Subjects</title>
                </head>
                <body>
                    <h1>Subjects</h1>
                    <table border="1" cellpadding="5" cellspacing="0">
                        <tr>
                            <th>Name</th>
                            <th>Marks</th>
                        </tr>
            """
            for subject in self._subjects.values():
                marks = ", ".join(subject['marks'])
                html += f"""
                        <tr>
                            <td>{subject['name']}</td>
                            <td>{marks}</td>
                        </tr>
                """
            html += """
                    </table>
                </body>
            </html>
            """
            return Response(200, "OK", headers={"Content-Type": "text/html"}, body=html)
    
        def handle_get_subject_by_id(self, subject_id):
            try:
                subject_id = int(subject_id)
                subject = self._subjects.get(subject_id)
                if not subject:
                    return Response(404, "Not Found", body="Subject not found")
    
                body = f"Name: {subject['name']}, Mark: {subject['mark']}"
                return Response(200, "OK", headers={"Content-Type": "text/plain"}, body=body)
    
            except ValueError:
                return Response(400, "Bad Request", body="Invalid subject ID")
    
        def send_response(self, conn, resp):
            status_line = f"HTTP/1.1 {resp.status} {resp.reason}\r\n"
            conn.sendall(status_line.encode('iso-8859-1'))
            for header, value in (resp.headers or {}).items():
                conn.sendall(f"{header}: {value}\r\n".encode('iso-8859-1'))
            conn.sendall(b"\r\n")
            if resp.body:
                conn.sendall(resp.body.encode('iso-8859-1'))
    
        def send_error(self, conn, err):
            status_code = 500
            reason = "Internal Server Error"
            if isinstance(err, ValueError):
                status_code = 400
                reason = str(err)
            elif isinstance(err, Exception):
                reason = str(err)
    
            print(f"Error: {err}")
    
            status_line = f"HTTP/1.1 {status_code} {reason}\r\n"
            conn.sendall(status_line.encode('iso-8859-1'))
            conn.sendall(b"\r\n")
            conn.sendall(f"{reason}\r\n".encode('iso-8859-1'))
    
    
    class Request:
        def __init__(self, method, target, headers, rfile):
            self.method = method
            self.path = target
            self.headers = headers
            self.rfile = rfile
    
    
    class Response:
        def __init__(self, status, reason, headers=None, body=None):
            self.status = status
            self.reason = reason
            self.headers = headers or {}
            self.body = body
    
    
    if __name__ == '__main__':
        server = MyHTTPServer()
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("Server stopped.")