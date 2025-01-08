# **Задание 5**
Написать простой веб-сервер для обработки GET и POST HTTP-запросов с помощью библиотеки socket в Python.

## **Требования:**
Сервер должен:

- Принять и записать информацию о дисциплине и оценке по дисциплине.

- Отдать информацию обо всех оценках по дисциплинам в виде HTML-страницы.

## **Серверная часть:**
Для того чтобы данные обработались корректно, я увеличила размер буфера до 4096 байт и, таким образом, уменьшила количество операций по чтению данных - это помогло избежать "падений" локалхоста. Также для избежания ошибок при POST-запросе была добавлена проверка на наличие тела у запроса - если оно неполное, читаем данные до тех пор, пока весь запрос не будет считан. Чтобы понять, сколько байтов понадобиться прочитать, я извлекла данные из клиентского запроса, который содержал количество байт при отправке. 

Добавление данных: если дисциплина и оценка не пустые, они добавляются в словарь `current_grades`. Если дисциплина уже есть в словаре, оценка добавляется к списку существующих оценок, если нет — создаётся новый список.


```python
import socket
from urllib.parse import parse_qs

# Хранилище для оценок в виде словаря
current_grades = {}

def load_html():
    with open('index2.html', 'r', encoding='utf-8') as file:
        return file.read()

def create_html():
    html_template = load_html()

    # Формирование списка оценок
    if current_grades:
        grades_list = ""
        for discipline, di_grades in current_grades.items():
            grades_str = ', '.join(di_grades)
            grades_list += f"<li>{discipline}: {grades_str}</li>"
    else:
        grades_list = "<li>Журнал пуст</li>"

    # Замена на реальный список оценок
    html_content = html_template.replace('{{grades_list}}', grades_list)
    return html_content


# Создание сокета
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8080))
server_socket.listen(1)

print("Сервер запущен на http://localhost:8080")

while True:
    client_socket, addr = server_socket.accept()
    request = client_socket.recv(4096).decode()  # Увеличиваем буфер для чтения

    # Получение метода запроса и пути
    request_line = request.splitlines()[0]
    method, path, _ = request_line.split()

    if method == 'GET':
        # Формируем ответ для GET-запроса
        response_body = create_html()
        response = 'HTTP/1.1 200 OK\nContent-Type: text/html; charset=utf-8\n\n' + response_body

    elif method == 'POST':
        # Проверяем, есть ли тело в запросе
        if '\r\n\r\n' in request:
            headers, body = request.split('\r\n\r\n', 1)
        else:
            headers, body = request, ''

        # Извлекаем длину
        content_length = 0
        for header in headers.splitlines():
            if 'Content-Length' in header:
                content_length = int(header.split(':')[1].strip())

        # Если тело неполное, ждем оставшиеся данные
        while len(body) < content_length:
            body += client_socket.recv(4096).decode()

        # Получение данных из POST-запроса
        data = parse_qs(body)

        # Записываем дисциплину и оценку
        subject = data.get('subject', [''])[0].strip()
        grade = data.get('grade', [''])[0].strip()

        if subject and grade:
            # Если дисциплина уже существует, добавляем новую оценку в список
            if subject in current_grades:
                current_grades[subject].append(grade)
            else:
                current_grades[subject] = [grade]

        response_body = create_html()
        response = 'HTTP/1.1 200 OK\nContent-Type: text/html; charset=utf-8\n\n' + response_body

    else:
        response = 'HTTP/1.1 405 Method Not Allowed\n\n'

    client_socket.sendall(response.encode('utf-8'))
    client_socket.close()
```

## **Код HTML-страницы:**

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Журнал оценок</title>
    <style>
        body {
            font-family: "Times New Roman", sans-serif;
            background-color: #f9f9f9;
            margin: 0;
            padding: 20px;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        h1 {
            color: #333;
        }
        .container {
            max-width: 400px;
            width: 100%;
            background-color: white;
            padding: 20px;
            border-radius: 4px;
            border: 1px solid #ccc;
            box-sizing: border-box;
        }
        input[type="text"] {
            width: 100%;
            padding: 8px;
            margin: 10px 0;
            border: 1px solid #ccc;
            border-radius: 4px;
            box-sizing: border-box;
        }
        input[type="submit"] {
            background-color: #007bff;
            color: white;
            padding: 10px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            width: 100%;
        }
        input[type="submit"]:hover {
            background-color: #0056b3;
        }
        ul {
            list-style-type: none;
            padding: 0;
            margin: 20px 0 0;
            background: white;
            border: 1px solid #ccc;
            border-radius: 4px;
            padding: 10px;
            box-sizing: border-box;
            width: 100%;
        }
        li {
            margin: 5px 0;
            padding: 5px 10px;
            border-bottom: 1px solid #ddd;
        }
        li:last-child {
            border-bottom: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Журнал оценок</h1>
        <form method="POST" action="/">
            Дисциплина: <input type="text" name="subject" placeholder="Название дисциплины"><br>
            Оценка: <input type="text" name="grade" placeholder="Оценка"><br>
            <input type="submit" value="Добавить">
        </form>

        <h2>Список оценок:</h2>
        <ul>
            {{grades_list}}
        </ul>
    </div>
</body>
</html>
```
