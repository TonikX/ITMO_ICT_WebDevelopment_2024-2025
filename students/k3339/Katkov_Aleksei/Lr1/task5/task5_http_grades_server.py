import socket
import json
import os
from urllib.parse import parse_qs

HOST = "127.0.0.1"
PORT = 8081
BUFFER_SIZE = 8192
FILE = "grades.json"

def load_data():
    if os.path.exists(FILE):
        with open(FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def build_html(data):
    rows = ""
    for subject, grades in data.items():
        pretty_grades = ", ".join(grades)
        rows += f"<tr><td>{subject}</td><td>{pretty_grades}</td></tr>"

    html = f"""
    <html>
    <head>
        <meta charset="utf-8">
        <title>Журнал</title>
    </head>
    <body>
        <h1>Журнал оценок</h1>

        <form method="POST">
            <label>Предмет:</label>
            <input name="subject"><br><br>

            <label>Оценка:</label>
            <input name="grade"><br><br>

            <button type="submit">Сохранить</button>
        </form>

        <hr>

        <table border="1" cellpadding="6">
            <tr>
                <th>Дисциплина</th>
                <th>Оценки</th>
            </tr>
            {rows}
        </table>

    </body>
    </html>
    """
    return html.encode()


def main():
    data = load_data()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"Журнал доступен: http://{HOST}:{PORT}")

    while True:
        conn, _ = server.accept()
        request = conn.recv(BUFFER_SIZE).decode()

        if request.startswith("POST"):
            body = request.split("\r\n\r\n")[1]
            params = parse_qs(body)

            raw_subject = params.get("subject", [""])[0]
            subject = raw_subject.strip().lower().replace("!", "").replace(".", "")
            subject = subject.capitalize()

            grade = params.get("grade", [""])[0].strip()

            if subject and grade:
                if subject not in data:
                    data[subject] = []
                data[subject].append(grade)
                save_data(data)

            response = (
                "HTTP/1.1 302 Found\r\n"
                "Location: /\r\n\r\n"
            ).encode()
            conn.sendall(response)

        else:
            body = build_html(data)
            response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/html; charset=utf-8\r\n"
                f"Content-Length: {len(body)}\r\n"
                "Connection: close\r\n\r\n"
            ).encode() + body

            conn.sendall(response)

        conn.close()

if __name__ == "__main__":
    main()
