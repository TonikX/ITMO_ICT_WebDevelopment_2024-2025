import socket
from urllib.parse import urlparse, parse_qs

HOST = "localhost"
PORT = 8080

# Хранилище оценок: {"Предмет": ["оценка1", "оценка2", ...]}
grades = {}

def build_page(message="", show_grades=False):
    html = """
    <html>
    <head><meta charset="UTF-8"><title>Оценки</title></head>
    <body>
        <h1>Добавление оценки</h1>
        <form method="POST" action="/">
            Дисциплина: <input type="text" name="subject"><br>
            Оценка: <input type="text" name="grade"><br>
            <button type="submit">Добавить оценку</button>
        </form>
    """

    if message:
        html += f"<p style='color:green;'>{message}</p>"

    html += """
        <form method="GET" action="/">
            <input type="hidden" name="show" value="1">
            <button type="submit">Показать текущие оценки</button>
        </form>
    """

    if show_grades:
        html += "<h2>Текущие оценки:</h2><ul>"
        for subject, subject_grades in grades.items():
            html += f"<li>{subject} — {', '.join(subject_grades)}</li>"
        html += "</ul>"

    html += "</body></html>"
    return html

def handle_request(request: str):
    try:
        method, path, _ = request.split(" ", 2)
    except ValueError:
        return "HTTP/1.1 400 Bad Request\r\n\r\nОшибка запроса"

    message = ""
    show_grades = False

    if method == "POST":
        headers, body = request.split("\r\n\r\n", 1)
        params = parse_qs(body)
        subject = params.get("subject", [""])[0].strip()
        grade = params.get("grade", [""])[0].strip()
        if subject and grade:
            grades.setdefault(subject, []).append(grade)
            message = "Оценка сохранена!"

    elif method == "GET":
        parsed = urlparse(path)
        params = parse_qs(parsed.query)
        if "show" in params:
            show_grades = True

    body = build_page(message=message, show_grades=show_grades)
    response = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html; charset=utf-8\r\n"
        f"Content-Length: {len(body.encode('utf-8'))}\r\n"
        "\r\n"
        f"{body}"
    )
    return response

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Сервер запущен на http://{HOST}:{PORT}")

    while True:
        conn, addr = server_socket.accept()
        request = conn.recv(1024).decode("utf-8")
        if not request:
            conn.close()
            continue
        print("Запрос:\n", request)

        response = handle_request(request)
        conn.sendall(response.encode("utf-8"))
        conn.close()

if __name__ == "__main__":
    start_server()
