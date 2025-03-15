import socket

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 8080
BUFFER_SIZE = 1024


grades = []

def handle_get():
    """Обрабатывает GET-запрос и формирует HTML-страницу с оценками."""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Оценки</title>
    </head>
    <body>
        <h1>Список оценок</h1>
        <table border="1">
            <tr>
                <th>Дисциплина</th>
                <th>Оценка</th>
            </tr>
    """
    for discipline, grade in grades:
        html_content += f"""
            <tr>
                <td>{discipline}</td>
                <td>{grade}</td>
            </tr>
        """
    html_content += """
        </table>
        <form method="POST" action="/">
            <h2>Добавить оценку</h2>
            <label>Дисциплина: <input type="text" name="discipline"></label><br>
            <label>Оценка: <input type="text" name="grade"></label><br>
            <button type="submit">Добавить</button>
        </form>
    </body>
    </html>
    """
    return (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html; charset=utf-8\r\n"
        f"Content-Length: {len(html_content.encode('utf-8'))}\r\n"
        "\r\n"
        + html_content
    )

def handle_post(request):
    """Обрабатывает POST-запрос и добавляет данные в хранилище."""
    body = request.split("\r\n\r\n", 1)[1]  # Получаем тело запроса
    params = dict(param.split("=") for param in body.split("&"))
    discipline = params.get("discipline", "").replace("+", " ")
    grade = params.get("grade", "").replace("+", " ")
    if discipline and grade:
        grades.append((discipline, grade))
    return (
        "HTTP/1.1 303 See Other\r\n"
        "Location: /\r\n"
        "\r\n"
    )

def tcp_server():
    """Запуск веб-сервера."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((SERVER_HOST, SERVER_PORT))
        server_socket.listen(1)
        print(f"Сервер запущен на http://{SERVER_HOST}:{SERVER_PORT}")

        while True:
            conn, addr = server_socket.accept()
            with conn:
                request = conn.recv(BUFFER_SIZE).decode()
                if not request:
                    continue

                headers = request.split("\r\n")
                method, path, _ = headers[0].split()

                if method == "GET":
                    response = handle_get()
                elif method == "POST":
                    response = handle_post(request)
                else:
                    response = (
                        "HTTP/1.1 405 Method Not Allowed\r\n"
                        "Content-Length: 0\r\n"
                        "\r\n"
                    )

                conn.sendall(response.encode())

if __name__ == "__main__":
    tcp_server()
