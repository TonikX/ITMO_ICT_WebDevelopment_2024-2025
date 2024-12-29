# Задание 5

Написать простой веб-сервер для обработки GET и POST HTTP-запросов с помощью библиотеки socket в Python.

Сервер должен:

1. Принять и записать информацию о дисциплине и оценке по дисциплине.
2. Отдать информацию обо всех оценках по дисциплинам в виде HTML-страницы.

## Реализация
Для начала создается сокет-сервер, который обрабатывает сетевые соединения и позволяет серверу взаимодействовать с клиентами по протоколу TCP. 
Сервер обрабатывает запросы, используя методы HTTP. Сервер хранит информацию о дисциплинах и оценках и отображает их на веб-странице в виде таблицы. При отправке формы с предметом и оценкой через POST-запрос, сервер добавляет данные в список и обновляет страницу с актуальной информацией. 

В итоге, сервер создает веб-приложение, позволяющее пользователю вводить и просматривать оценки по дисциплинам в интерактивном формате.
### Код
```python
import socket
from urllib.parse import unquote

grades = []


def generate_html_page():
    html = """
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Оценки</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f4f4f9;
            }
            .container {
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                background-color: #fff;
                border-radius: 10px;
            }
            h1 {
                text-align: center;
                color: #333;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
            }
            table, th, td {
                border: 1px solid #ddd;
            }
            th, td {
                padding: 12px;
                text-align: left;
            }
            th {
                background-color: #f2f2f2;
                font-weight: bold;
            }
            }
            form {
                margin-top: 20px;
                text-align: center;
            }
            label {
                font-weight: bold;
                margin-right: 10px;
            }
            input[type="text"] {
                padding: 8px;
                margin-right: 10px;
                border: 1px solid #ccc;
                border-radius: 4px;
                width: 200px;
            }
            input[type="submit"] {
                background-color: #8b00ff;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
            }
            input[type="submit"]:hover {
                background-color: #9c80f7;
            }
        </style>
    </head>
    <body>
    <div class="container">
        <h1>Зачетка</h1>
    """

    if grades:
        html += """
        <table>
            <tr>
                <th>Дисциплина</th>
                <th>Оценка</th>
            </tr>
        """
        for subject, grade in grades:
            html += f"<tr><td>{subject}</td><td>{grade}</td></tr>"
        html += "</table>"
    else:
        html += "<p>Нет данных об оценивании.</p>"

    html += """
        <form action="/" method="POST">
            <label>Предмет: <input type="text" name="subject" required></label>
            <label>Оценка: <input type="text" name="grade" required></label>
            <input type="submit" value="Внести данные">
        </form>
    </div>
    </body>
    </html>
    """
    return html


def parse_post_data(data):
    post_data = data.split("&")
    subject = ""
    grade = ""
    for pair in post_data:
        key, value = pair.split("=")
        if key == "subject":
            subject = unquote(value)  # Декодируем URL-кодированное значение
        elif key == "grade":
            grade = unquote(value)  # Декодируем URL-кодированное значение
    return subject, grade


def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 8080))
    server_socket.listen(1)

    print("Server is running on http://localhost:8080...")

    while True:
        client_socket, addr = server_socket.accept()
        request = client_socket.recv(1024).decode()

        headers = request.split("\n")
        method = headers[0].split(" ")[0]

        if method == "GET":
            response_body = generate_html_page()
            response = "HTTP/1.1 200 OK\nContent-Type: text/html; charset=UTF-8\n\n" + response_body
        elif method == "POST":
            content_length = 0
            for header in headers:
                if "Content-Length" in header:
                    content_length = int(header.split(":")[1].strip())
                    break

            body = request.split("\r\n\r\n")[1][:content_length]

            subject, grade = parse_post_data(body)
            if subject and grade:
                grades.append((subject, grade))

            response_body = generate_html_page()
            response = "HTTP/1.1 200 OK\nContent-Type: text/html; charset=UTF-8\n\n" + response_body

        client_socket.sendall(response.encode('utf-8'))
        client_socket.close()

run_server()

```