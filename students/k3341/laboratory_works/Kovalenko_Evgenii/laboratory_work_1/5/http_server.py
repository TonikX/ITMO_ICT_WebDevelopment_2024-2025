from socket import socket, AF_INET, SOCK_STREAM
from sys import exit
from urllib.parse import parse_qs, unquote


class MyHTTPServer:
    def __init__(self, host: str, port: int, server_name: str) -> None:
        self.host = host
        self.port = port
        self.server_name = server_name
        self.grades = {}  # Словарь для хранения оценок {дисциплина: [оценки]}

    def serve_forever(self) -> None:
        # Запуск сервера на сокете, обработка входящих соединений
        server_socket = socket(AF_INET, SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)

        print(f"Сервер {self.server_name} запущен на http://{self.host}:{self.port}")
        print("Ожидание подключений...")

        while True:
            client_socket, client_address = server_socket.accept()
            print(f'Подключение от {client_address}')
            self.serve_client(client_socket)

    def serve_client(self, client_socket: socket) -> None:
        # Обработка клиентского подключения
        try:
            # Читаем весь запрос
            request_data = b""
            while True:
                chunk = client_socket.recv(4096)
                if not chunk:
                    break
                request_data += chunk
                # Проверяем, достигли ли конца запроса
                if b"\r\n\r\n" in request_data:
                    # Если есть Content-Length, читаем тело полностью
                    headers = request_data.split(b"\r\n\r\n")[0].decode()
                    if "Content-Length:" in headers:
                        content_length = int(headers.split("Content-Length:")[1].split("\r\n")[0].strip())
                        body_start = request_data.find(b"\r\n\r\n") + 4
                        if len(request_data) < body_start + content_length:
                            # Дорешиваем тело
                            remaining = body_start + content_length - len(request_data)
                            request_data += client_socket.recv(remaining)
                    break

            request = request_data.decode('utf-8')
            if not request:
                return

            # Парсим запрос
            method, url, version = self.parse_request(request)

            # Обрабатываем запрос
            response = self.handle_request(method, request)

            # Отправляем ответ
            self.send_response(client_socket, response)

        except Exception as e:
            print(f"Ошибка обработки запроса: {e}")
            error_response = ("HTTP/1.1 500 Internal Server Error\r\n"
                              "\r\n"
                              "<h1>500 Internal Server Error</h1>")
            client_socket.send(error_response.encode('utf-8'))
        finally:
            client_socket.close()

    def parse_request(self, request: str) -> tuple[str, str, str]:
        # Обработка заголовка http+запроса
        lines = request.split('\r\n')
        if not lines:
            raise ValueError("Пустой запрос")

        # Первая строка: метод + url + версия протокола
        first_line = lines[0].split(' ')
        if len(first_line) < 3:
            raise ValueError("Неверный формат запроса")

        method, url, version = first_line[0], first_line[1], first_line[2]
        return method, url, version

    def handle_request(self, method: str, request: str) -> str:
        # Обработка url в соответствии с нужным методом
        if method == 'GET':
            return self.handle_get()
        elif method == 'POST':
            return self.handle_post(request)
        else:
            return ("HTTP/1.1 405 Method Not Allowed\r\n"
                    "\r\n"
                    "<h1>405 Method Not Allowed</h1>")

    def handle_get(self) -> str:
        # Генерация HTML-страницы с оценками
        html = self.generate_html()
        html_bytes = html.encode('utf-8')
        response = (f"HTTP/1.1 200 OK\r\n"
                    f"Content-Type: text/html; charset=utf-8\r\n"
                    f"Content-Length: {len(html_bytes)}\r\n"
                    f"\r\n"
                    f"{html}")
        return response

    def handle_post(self, request: str) -> str:
        # Обработка POST-запроса (добавление оценки)
        try:
            # Извлекаем тело запроса
            lines = request.split('\r\n')
            empty_line_index = -1
            for i, line in enumerate(lines):
                if line == '':
                    empty_line_index = i
                    break

            if empty_line_index != -1 and empty_line_index + 1 < len(lines):
                body = '\r\n'.join(lines[empty_line_index + 1:])
                params = parse_qs(body)

                subject = unquote(params.get('subject', [''])[0])
                grade_str = unquote(params.get('grade', [''])[0])

                if subject and grade_str:
                    try:
                        grade = int(grade_str)
                        if 1 <= grade <= 5:
                            if subject not in self.grades:
                                self.grades[subject] = []
                            self.grades[subject].append(grade)
                            print(f"Добавлена оценка: {subject} - {grade}")
                    except ValueError:
                        print(f"Ошибка преобразования оценки: {grade_str}")

            # После POST-запроса делаем редирект на главную страницу
            return ("HTTP/1.1 303 See Other\r\n"
                    "Location: /\r\n"
                    "\r\n")

        except Exception as e:
            print(f"Ошибка обработки POST-запроса: {e}")
            return ("HTTP/1.1 400 Bad Request\r\n"
                    "\r\n"
                    "<h1>400 Bad Request</h1>")

    def generate_html(self) -> str:
        """Генерация HTML-страницы с оценками"""
        html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Оценки по дисциплинам - {self.server_name}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        h1 {{ color: #333; }}
        form {{ margin-bottom: 20px; padding: 15px; background: #f5f5f5; border-radius: 5px; }}
        table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
        input, button {{ padding: 8px; margin: 5px; }}
    </style>
</head>
<body>
    <h1>Система учета оценок</h1>

    <form method="POST">
        <h3>Добавить оценку</h3>
        <input type="text" name="subject" placeholder="Дисциплина" required>
        <input type="number" name="grade" placeholder="Оценка" min="1" max="5" required>
        <button type="submit">Добавить</button>
    </form>

    <h2>Список оценок</h2>"""

        if self.grades:
            html += """
    <table>
        <tr>
            <th>Дисциплина</th>
            <th>Оценки</th>
            <th>Средний балл</th>
        </tr>"""

            for subject, grades_list in self.grades.items():
                avg_grade = sum(grades_list) / len(grades_list) if grades_list else 0
                html += f"""
        <tr>
            <td>{subject}</td>
            <td>{', '.join(map(str, grades_list))}</td>
            <td>{avg_grade:.2f}</td>
        </tr>"""

            html += """
    </table>"""
        else:
            html += """
    <p>Пока нет оценок. Добавьте первую оценку!</p>"""

        html += """
</body>
</html>"""

        return html

    def send_response(self, client_socket: socket, response: str) -> None:
        # Отправка ответа
        client_socket.send(response.encode('utf-8'))


if __name__ == '__main__':
    serv = MyHTTPServer('localhost', 8080, 'GradeServer')
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("\nСервер остановлен")
        exit(0)