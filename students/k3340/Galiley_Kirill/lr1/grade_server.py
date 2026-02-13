import socket
from urllib.parse import parse_qs

HOST = "127.0.0.1"
PORT = 5004

grades = []  # список словарей: {"subject": ..., "grade": ...}

def build_html():
    rows = ""
    for g in grades:
        rows += f"<tr><td>{g['subject']}</td><td>{g['grade']}</td></tr>"
    return f"""
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Оценки</title>
</head>
<body>
    <h1>Список оценок</h1>
    <form method="POST" action="/">
        Дисциплина: <input type="text" name="subject">
        Оценка: <input type="text" name="grade">
        <button type="submit">Сохранить</button>
    </form>
    <table border="1" cellpadding="5">
        <tr><th>Дисциплина</th><th>Оценка</th></tr>
        {rows}
    </table>
</body>
</html>
"""

def build_response(body: str) -> bytes:
    body_bytes = body.encode("utf-8")
    headers = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html; charset=utf-8\r\n"
        f"Content-Length: {len(body_bytes)}\r\n"
        "Connection: close\r\n"
        "\r\n"
    )
    return headers.encode("utf-8") + body_bytes

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(5)
    print(f"Grade HTTP server on {HOST}:{PORT}")
    while True:
        conn, addr = s.accept()
        with conn:
            request = conn.recv(4096).decode("utf-8", errors="ignore")
            if not request:
                continue

            first_line = request.splitlines()[0]
            method, path, _ = first_line.split()

            if method == "POST":
                parts = request.split("\r\n\r\n", 1)
                body = parts[1] if len(parts) > 1 else ""
                data = parse_qs(body)
                subject = data.get("subject", [""])[0]
                grade = data.get("grade", [""])[0]
                if subject and grade:
                    grades.append({"subject": subject, "grade": grade})

            html = build_html()
            response = build_response(html)
            conn.sendall(response)
