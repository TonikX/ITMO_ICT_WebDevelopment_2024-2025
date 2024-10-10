### Задание

Написать простой веб-сервер для обработки GET и POST HTTP-запросов с помощью библиотеки socket в Python.

Сервер должен:
1. Принять и записать информацию о дисциплине и оценке по дисциплине.
2. Отдать информацию обо всех оценках по дисциплинам в виде HTML-страницы.
### `server.py`

```python
import socket


class MyHTTPServer:
    def __init__(self, host='127.0.0.1', port=8090):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Сервер запущен на {self.host}:{self.port}")

        self.grades = {}

    def serve_forever(self):
        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                self.serve_client(client_socket)
        except KeyboardInterrupt:
            print("\nОстановка сервера.")
        finally:
            self.server_socket.close()

    def serve_client(self, client_socket):
        try:
            while True:
                request = client_socket.recv(1024).decode('utf-8')
                if not request:
                    return

                method, url, headers, body = self.parse_request(request)

                if method == "GET":
                    self.handle_get(client_socket)
                elif method == "POST":
                    self.handle_post(client_socket, body)
                else:
                    self.send_response(client_socket, "405 Method Not Allowed", "Метод не поддерживается.")
        finally:
            client_socket.close()

    def parse_request(self, request):
        lines = request.split("\r\n")
        method, url, protocol = lines[0].split(" ")

        headers = {}
        body = ''
        i = 1
        # Считываем заголовки
        while lines[i]:
            if ": " in lines[i]:
                key, value = lines[i].split(": ", 1)
                headers[key] = value
            i += 1
        if i < len(lines) - 1:
            body = lines[i + 1]

        print(body)
        return method, url, headers, body

    def handle_get(self, client_socket):
        response_body = "<html><body><h1>Оценки по дисциплинам</h1><ul>"
        for discipline in self.grades.keys():
            response_body += f"<li>{discipline}:"
            for grade in self.grades[discipline]:
                response_body += f" {grade},"
            response_body = response_body[:len(response_body)-1]
            response_body += "</li>"

        response_body += "</ul>"

        response_body += """
                <h2>Добавить новую оценку</h2>
                <form method="POST" action="/">
                    <label for="discipline">Дисциплина:</label><br>
                    <input type="text" id="discipline" name="discipline"><br>
                    <label for="grade">Оценка:</label><br>
                    <input type="text" id="grade" name="grade"><br><br>
                    <input type="submit" value="Добавить">
                </form>
                """

        response_body += "</body></html>"

        self.send_response(client_socket, "200 OK", response_body)

    def handle_post(self, client_socket, body):
        # discipline=<название>&grade=<оценка>
        params = {}
        for pair in body.split("&"):
            key, value = pair.split("=")
            params[key] = value

        discipline = params.get('discipline', '').replace('+', ' ')
        grade = params.get('grade', '')

        if discipline and grade:
            if discipline in self.grades:
                self.grades[discipline].append(grade)
            else:
                self.grades[discipline] = [grade]
            self.handle_get(client_socket)
        else:
            self.send_response(client_socket, "400 Bad Request", "<html><body><h1>Неверный запрос!</h1><a "
                                                                 "href='/'>Назад</a></body></html>")

    def send_response(self, client_socket, status, body):
        response = f"HTTP/1.1 {status}\r\n"
        response += "Content-Type: text/html; charset=utf-8\r\n"
        response += f"Content-Length: {len(body.encode('utf-8'))}\r\n"
        response += "Connection: close\r\n"
        response += "\r\n"
        response += body

        client_socket.sendall(response.encode('utf-8'))


if __name__ == '__main__':
    server = MyHTTPServer(host='127.0.0.1', port=8090)
    server.serve_forever()

```

Сервер создает сокет, работающий по протоколу TCP и ожидает запроса от клиента. Клиент направляет запрос GET или POST. Запрос парсится (считываются заголовки и тело), далее направляется в соответствующий хэндлер.

При POST-запросе считываются параметры дисциплины и оценки и добавляются в словарь успеваемости. При GET-запросе составляется html ответ, содержащий каждую дисциплину со всеми сохраненными оценками.

Ссылка на хост:
http://127.0.0.1:8090/

В случае ошибки команды curl:

```Remove-item alias:curl```

Пример POST-запроса: 

```curl -X POST -d "discipline=math&grade=5" http://127.0.0.1:8090```
