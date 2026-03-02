# Задание
Написать простой веб-сервер для обработки GET и POST HTTP-запросов с помощью библиотеки socket в Python.

**Требования:**

- Принять и записать информацию о дисциплине и оценке по дисциплине.
- Отдать информацию обо всех оценках по дисциплинам в виде HTML-страницы.
 
***

# Решение

## Сервер

```python
import socket
from urllib.parse import parse_qs

HOST = 'localhost'
PORT = 9090

grades = []


def handle_request(request):
    lines = request.split('\r\n')
    if not lines:
        return "HTTP/1.1 400 Bad Request\r\n\r\n"

    try:
        method, path, _ = lines[0].split()
    except ValueError:
        return "HTTP/1.1 400 Bad Request\r\n\r\n"

    if method == "GET":
        response_body = """
        <html>
        <head>
            <title>Оценки</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                }
                table {
                    border-collapse: collapse;
                    width: 50%;
                }
                th, td {
                    border: 1px solid black;
                    padding: 8px;
                    text-align: center;
                }
                th {
                    background-color: #f2f2f2;
                }
                h2, h3 {
                    margin-top: 20px;
                }
            </style>
        </head>
        <body>
        <h2>Оценки по дисциплинам</h2>

        <table>
            <tr>
                <th>Дисциплина</th>
                <th>Оценка</th>
            </tr>
        """

        for grade in grades:
            response_body += f"""
            <tr>
                <td>{grade['subject']}</td>
                <td>{grade['mark']}</td>
            </tr>
            """

        response_body += """
        </table>
        <h3>Добавить новую оценку</h3>
        <form method="POST">
            Дисциплина: <input name="subject" required><br><br>
            Оценка: <input name="mark" required><br><br>
            <input type="submit" value="Добавить">
        </form>

        </body>
        </html>
        """

        response = (
            "HTTP/1.1 200 OK\r\n"
            f"Content-Length: {len(response_body.encode('utf-8'))}\r\n"
            "Content-Type: text/html; charset=utf-8\r\n"
            "\r\n"
            + response_body
        )
        return response

    elif method == "POST":
        try:
            empty_line = lines.index('')
            body = '\r\n'.join(lines[empty_line + 1:])
        except ValueError:
            body = lines[-1]

        data = parse_qs(body)
        subject = data.get("subject", [""])[0]
        mark = data.get("mark", [""])[0]

        if subject and mark:
            grades.append({
                "subject": subject,
                "mark": mark
            })

        response = (
            "HTTP/1.1 303 See Other\r\n"
            "Location: /\r\n"
            "Content-Length: 0\r\n"
            "\r\n"
        )
        return response

    else:
        return "HTTP/1.1 405 Method Not Allowed\r\n\r\n"


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(1)

    print(f"Server started on http://{HOST}:{PORT}")
    print("Open this link in your browser")

    while True:
        conn, addr = sock.accept()
        print("Connected:", addr)

        request = b""
        while True:
            part = conn.recv(1024)
            if not part:
                break
            request += part
            if len(part) < 1024:
                break

        request = request.decode('utf-8', errors='ignore')
        print("Request received:\n", request)

        response = handle_request(request)
        conn.sendall(response.encode('utf-8'))
        conn.close()


if __name__ == "__main__":
    main()
```
***

# Пояснение

# Веб-сервер для хранения оценок на Python

Этот код реализует простой HTTP-сервер, который позволяет просматривать и добавлять оценки через веб-интерфейс.

## Принцип работы

1. Сервер запускается и слушает локальный порт 9090
2. При переходе в браузере на `http://localhost:9090` открывается страница со списком оценок
3. Через форму можно добавить новую оценку (предмет и оценку)
4. Все данные хранятся в оперативной памяти (список `grades`)

## Как это работает

### GET-запрос
- Сервер отдаёт HTML-страницу со списком всех сохранённых оценок
- Внизу страницы находится форма для добавления новой оценки

### POST-запрос
- Когда пользователь отправляет форму, сервер получает данные
- Извлекает предмет (`subject`) и оценку (`mark`)
- Добавляет их в список `grades`
- Перенаправляет обратно на главную страницу (код 303)

## Основные функции

- **`handle_request(request)`** — разбирает HTTP-запрос и формирует ответ
- **`main()`** — главный цикл сервера, принимает подключения

## Особенности реализации

- Сервер обрабатывает только GET и POST методы
- Данные формы разбираются через `urllib.parse.parse_qs`
- При добавлении оценки происходит редирект (чтобы избежать повторной отправки при обновлении)
- Все ответы возвращаются в кодировке UTF-8
- Сервер обрабатывает одно подключение за раз (без многопоточности)

## Формат хранения

Оценки хранятся как список словарей:
```python
grades = [
    {"subject": "Математика", "mark": "5"},
    {"subject": "Физика", "mark": "4"}
]