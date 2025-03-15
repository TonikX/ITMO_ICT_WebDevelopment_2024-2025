import socket
import urllib.parse


class MyHTTPServer:
    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port
        self.grades = []  # Хранилище данных о дисциплинах и оценках

    def serve_forever(self) -> None:
        """
        Запускает сервер на заданном хосте и порте, обрабатывая входящие соединения.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.host, self.port))
            server_socket.listen(5)
            print(f'Сервер запущен на {self.host}:{self.port}')

            while True:
                client_socket, client_address = server_socket.accept()
                print(f'Подключение от {client_address}')
                self.serve_client(client_socket)

    def serve_client(self, client_socket: socket.socket) -> None:
        """
        Обрабатывает одно клиентское соединение.
        """
        with client_socket:
            request = client_socket.recv(1024).decode()
            if not request:
                return

            method, path, headers, body = self.parse_request(request)
            if method == 'GET':
                self.handle_get(client_socket)
            elif method == 'POST':
                self.handle_post(client_socket, body)
            else:
                self.send_response(client_socket, 405, 'Method Not Allowed', 'Метод не поддерживается.')

    def parse_request(self, request: str) -> tuple[str, str, dict, str]:
        """
        Парсит HTTP-запрос и возвращает метод, путь, заголовки и тело.
        """
        lines = request.split('\r\n')
        method, path, _ = lines[0].split(' ')
        headers = {}
        body = ''
        header_section = True

        for line in lines[1:]:
            if header_section:
                if line == '':
                    header_section = False
                else:
                    key, value = line.split(': ', 1)
                    headers[key] = value
            else:
                body += line

        return method, path, headers, body

    def handle_get(self, client_socket: socket.socket) -> None:
        """
        Обрабатывает GET-запрос, возвращая HTML-страницу с дисциплинами и оценками.
        """
        content = '<html><body><h1>Оценки</h1><ul>'
        for grade in self.grades:
            content += f"<li>{grade['discipline']}: {grade['grade']}</li>"
        content += "</ul><form method='POST' action='/'>"
        content += "<label>Дисциплина: <input type='text' name='discipline'></label><br>"
        content += "<label>Оценка: <input type='text' name='grade'></label><br>"
        content += "<button type='submit'>Добавить</button></form></body></html>"

        self.send_response(client_socket, 200, 'OK', content)

    def handle_post(self, client_socket: socket.socket, body: str) -> None:
        """
        Обрабатывает POST-запрос, добавляя новую дисциплину и оценку.
        """
        params = urllib.parse.parse_qs(body)
        discipline = params.get('discipline', [''])[0]
        grade = params.get('grade', [''])[0]

        if discipline and grade:
            self.grades.append({'discipline': discipline, 'grade': grade})
            self.send_response(client_socket, 303, 'See Other', '', headers={'Location': '/'})
        else:
            self.send_response(client_socket, 400, 'Bad Request', 'Поля дисциплины и оценки обязательны.')

    def send_response(self, client_socket: socket.socket, status_code: int, reason: str, content: str, headers: dict | None = None) -> None:
        """
        Отправляет HTTP-ответ клиенту.
        """
        if headers is None:
            headers = {}
        headers['Content-Length'] = len(content.encode())
        headers['Content-Type'] = 'text/html; charset=utf-8'

        response = f'HTTP/1.1 {status_code} {reason}\r\n'
        for key, value in headers.items():
            response += f'{key}: {value}\r\n'
        response += '\r\n'
        response += content

        client_socket.sendall(response.encode())


if __name__ == '__main__':
    host = 'localhost'
    port = 8080
    server = MyHTTPServer(host, port)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nСервер остановлен.')
