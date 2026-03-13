import socket
from urllib.parse import parse_qs

HOST = "127.0.0.1"
PORT = 8081

grades = {}

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)

print(f"Журнал на http://{HOST}:{PORT}")

def html():
    page = "<h1>Журнал оценок</h1>"
    for subj, marks in grades.items():
        page += f"<p>{subj}: {', '.join(marks)}</p>"

    page += """
    <form method="POST">
        Предмет: <input name="subject"><br>
        Оценка: <input name="grade"><br>
        <button type="submit">Добавить</button>
    </form>
    """
    return page

while True:
    conn, _ = server.accept()
    req = conn.recv(4096).decode()

    if "POST" in req:
        body = req.split("\r\n\r\n")[1]
        data = parse_qs(body)
        s = data.get("subject", [""])[0]
        g = data.get("grade", [""])[0]
        if s:
            grades.setdefault(s, []).append(g)

    response = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html; charset=utf-8\r\n\r\n"
        + html()
    )

    conn.send(response.encode())
    conn.close()