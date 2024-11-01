# Задание 5:
Написать простой веб-сервер для обработки GET и POST HTTP-запросов с помощью библиотеки socket в Python.

## Задание:

- Сервер должен:

1. Принять и записать информацию о дисциплине и оценке по дисциплине.
2. Отдать информацию обо всех оценках по дисциплинам в виде HTML-страницы.

### Серверная часть
Основной функционал включает:
1. Обработку GET-запросов для получения HTML-страницы со всеми оценками по дисциплинам.
2. Обработку POST-запросов для сохранения данных о дисциплине и оценке.

```python
import socket
from threading import Thread

grades = {}


def handle_client(client_sock):
    request = client_sock.recv(1024).decode()
    method, body, content_length = parse_request(request)
    print(f"Новый {method} запрос")

    if method == 'GET':
        response_body = generate_html()
        http_response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/html; charset=UTF-8\r\n"
                f"Content-Length: {len(response_body)}\r\n"
                "\r\n"
                + response_body
        )
        client_sock.sendall(http_response.encode())

    elif method == 'POST':
        data = body[:content_length]
        pairs = data.split('&')
        post_grades = {}

        for pair in pairs:
            key, value = pair.split('=')
            if key.startswith('subject'):
                subject_key = key
                subject_value = value
                post_grades[subject_key] = {'subject': subject_value, 'grade': None}
            if key.startswith('grade'):
                grade_key = key.replace('grade', 'subject')
                grade_value = value
                if grade_key in post_grades:
                    post_grades[grade_key]['grade'] = grade_value

            for key, value in post_grades.items():
                if value['subject'] and value['grade']:
                    grades[value['subject']] = value['grade']

        response = """HTTP/1.1 200 OK
        Content-Type: text/plain

        Data successfully saved."""
        client_sock.sendall(response.encode())

    client_sock.close()


def parse_request(request):
    parts = request.split('\r\n\r\n')
    headers = parts[0]
    body = parts[1] if len(parts) > 1 else ''
    method, path, version = headers.split('\r\n')[0].split(' ')
    content_length = 0
    content_length_header = [head for head in headers.split('\r\n') if "Content-Length" in head]
    if content_length_header:
        content_length = int(content_length_header[0].split(': ')[1])

    return method, body, content_length


def generate_html():
    sorted_grades = dict(sorted(grades.items()))
    html_text = """
    <html>
    <head><title>My grades</title></head>
    <body>
        <h2>Shalunov Andrei marks</h2>
        <table border="3">
            <tr>
                <th>Subject</th>
                <th>Grade</th>
            </tr>"""

    for subject, grade in sorted_grades.items():
        html_text += f"""
        <tr>
            <td>{subject}</td>
            <td>{grade}</td>
        """

    html_text += """
        </table>
    </body>
    </html>"""

    return html_text


HOST = 'localhost'
PORT = 8080

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen()

while True:
    connection, _ = sock.accept()
    thread = Thread(target=handle_client, args=(connection,))
    thread.start()
```

## Процесс выполнения:

1. Сервер запускается и ожидает подключений клиентов.
2. Клиент может отправить POST-запрос с информацией о дисциплине и оценке, например:

```
curl -X POST http://127.0.0.1:8080/ -d "subject=Mathematics&grade=5"
```
```
curl -X POST http://127.0.0.1:8080/ -d "subject1=Mathematics&grade1=5&subject2=Russian&grade2=4&subject3=Physics&grade3=3"
```

Сервер принимает эти данные и сохраняет оценку по указанной дисциплине.
Также сервер в ответ возвращает сообщение
```
HTTP/1.1 200 OK
Content-Type: text/plain

Data successfully saved.
```
3. Клиент может отправить GET-запрос для получения HTML-страницы со всеми дисциплинами и оценками:

```
GET / HTTP/1.1
```

Сервер формирует и отправляет HTML-страницу, которая содержит список дисциплин и соответствующих оценок в виде таблицы.

4. HTML-страница возвращает информацию:

```html
<!DOCTYPE html>
<html>
<head><title>My grades</title></head>
<body>
    <h2>Shalunov Andrei marks</h2>
    <table border="3">
        <tr>
            <th>Subject</th>
            <th>Grade</th>
        </tr>
        <tr>
            <td>{subject}</td>
            <td>{grade}</td>
        </tr>
    </table>
</body>
</html>
```