import socket
import urllib.parse

HOST = "127.0.0.1"
PORT = 50004

grades = {}  # дисциплина -> список оценок


def render_page():
    rows = ""
    for discipline, marks in grades.items():
        marks_str = ", ".join(marks)
        rows += f"<tr><td>{discipline}</td><td>{marks_str}</td></tr>"

    return f"""<!DOCTYPE html>
<html lang="ru">
<head><meta charset="UTF-8"><title>Журнал оценок</title></head>
<body>
    <h1>Журнал оценок</h1>
    <form method="POST" action="/">
        <input type="text" name="discipline" placeholder="Дисциплина" required>
        <input type="number" name="grade" placeholder="Оценка" min="2" max="5" required>
        <button type="submit">Добавить</button>
    </form>
    <table border="1" cellpadding="6">
        <tr><th>Дисциплина</th><th>Оценки</th></tr>
        {rows}
    </table>
</body>
</html>"""


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
server.settimeout(0.5)  # чтобы accept() не блокировал Ctrl+C навсегда
print(f"Сервер оценок запущен на http://{HOST}:{PORT}")

try:
    while True:
        try:
            conn, address = server.accept()
        except socket.timeout:
            continue

        request = conn.recv(1024).decode()

        if not request:
            conn.close()
            continue

        first_line = request.split("\r\n")[0]
        method, path, _ = first_line.split(" ")

        if method == "POST":
            headers_part, _, body = request.partition("\r\n\r\n")

            content_length = 0
            for line in headers_part.split("\r\n")[1:]:
                if line.lower().startswith("content-length"):
                    content_length = int(line.split(":")[1].strip())

            while len(body.encode()) < content_length:
                body += conn.recv(1024).decode()

            params = urllib.parse.parse_qs(body)
            discipline = params["discipline"][0]
            grade = params["grade"][0]
            grades.setdefault(discipline, []).append(grade)

        body_html = render_page().encode()
        headers = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html; charset=utf-8\r\n"
            f"Content-Length: {len(body_html)}\r\n"
            "\r\n"
        ).encode()

        conn.sendall(headers + body_html)
        conn.close()
except KeyboardInterrupt:
    print("\nСервер остановлен")
finally:
    server.close()
