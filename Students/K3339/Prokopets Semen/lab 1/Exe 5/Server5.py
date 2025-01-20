import socket
import urllib.parse

grades = []


def handle_request(request):
    global grades
    lines = request.splitlines()
    method = lines[0].split()[0]

    if method == "POST":
        # POST-запрос
        content_length = int([line for line in lines if line.startswith('Content-Length:')][0].split(': ')[1])

        if len(request.split('\r\n\r\n')) > 1:
            body = request.split('\r\n\r\n')[1][:content_length]
            parsed_body = urllib.parse.parse_qs(body)
            discipline = parsed_body.get('discipline', [''])[0]
            grade = parsed_body.get('grade', [''])[0]
            grades.append((discipline, grade))

            response_body = "<h1>Оценка добавлена!</h1><br>"
        else:
            response_body = "<h1>Ошибка: Тело запроса отсутствует!</h1><br>"

    elif method == "GET":
        # Формирование HTML-страницы с формой и списком оценок
        response_body = """
        <html>
            <head>
                <meta charset="UTF-8">
                <meta http-equiv="Content-Language" content="ru">
                <title>Список оценок</title>
            </head>
            <body>
                <h1>Добавить оценку</h1>
                <form method="POST" action="/">
                    Дисциплина: <input type="text" name="discipline"><br>
                    Оценка: <input type="text" name="grade"><br>
                    <input type="submit" value="Добавить">
                </form>
                <h1>Список оценок</h1>
                <ul>
        """
        for discipline, grade in grades:
            response_body += f"<li>{discipline}: {grade}</li>"

        response_body += """
                </ul>
            </body>
        </html>
        """

    else:
        response_body = "Метод не поддерживается."

    response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n{response_body}"
    return response


def run_server(host='127.0.0.1', port=8080):
    """Запускает веб-сервер."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"Сервер запущен на http://{host}:{port}/")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Подключение от {addr}")

        request = client_socket.recv(1024).decode('utf-8')
        print(f"Запрос: {request}")

        # Проверка на пустой запрос
        if not request.strip():
            print("Получен пустой запрос.")
            client_socket.close()
            continue

        response = handle_request(request)

        client_socket.sendall(response.encode('utf-8'))
        client_socket.close()


if __name__ == "__main__":
    run_server()