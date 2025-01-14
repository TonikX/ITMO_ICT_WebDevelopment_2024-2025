## Задание №5. Простой веб-сервер 

### Описание: 
Написать простой веб-сервер для обработки GET и POST HTTP-запросов с помощью библиотеки socket в Python.


### Требования:
Сервер должен:
* Принять и записать информацию о дисциплине и оценке по дисциплине.
* Отдать информацию обо всех оценках по дисциплинам в виде HTML-страницы.

### Листинг кода:
#### server.py
```
import socket
import threading


grades = {}


def generate_html():
    response = """
    <html>
    <head>
        <title>Disciplines grades</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 40px;
            }
            table {
                width: 50%;
                border-collapse: collapse;
                margin-bottom: 20px;
            }
            table, th, td {
                border: 1px solid #ddd;
            }
            th, td {
                padding: 10px;
                text-align: left;
            }
            th {
                background-color: #f2f2f2;
            }
            form {
                margin-top: 20px;
            }
            input[type="text"] {
                margin: 5px 0;
                padding: 5px;
                width: 200px;
            }
            input[type="submit"] {
                padding: 5px 15px;
                background-color: #4CAF50;
                color: white;
                border: none;
                cursor: pointer;
            }
        </style>
    </head>
    <body>
        <h1>Disciplines grades</h1>
        <table>
            <tr>
                <th>Discipline</th>
                <th>Grade</th>
            </tr>
    """
    for subject, grade_list in grades.items():
        grades_str = ', '.join(grade_list)
        response += f"<tr><td>{subject}</td><td>{grades_str}</td></tr>"

    response += """
        </table>
        <h2>Add new grade</h2>
        <form method="POST">
            Discipline: <input type="text" name="subject"><br>
            Grade: <input type="text" name="grade"><br>
            <input type="submit" value="Add">
        </form>
    </body>
    </html>
    """
    return response


def handle_client(client_socket):
    request = client_socket.recv(1024).decode()
    headers = request.split('\r\n')
    if len(headers) > 0:
        request_line = headers[0]
        method, path, _ = request_line.split()

        if method == 'GET':
            response_body = generate_html()
            response_headers = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
            client_socket.sendall((response_headers + response_body).encode())

        elif method == 'POST':
            body = request.split('\r\n\r\n')[1]
            params = dict(param.split('=') for param in body.split('&'))
            subject = params.get('subject', '').replace('+', ' ')
            grade = params.get('grade', '')
            if subject and grade:
                if subject in grades:
                    grades[subject].append(grade)
                else:
                    grades[subject] = [grade]

            response_headers = "HTTP/1.1 303 See Other\r\nLocation: /\r\n\r\n"
            client_socket.sendall(response_headers.encode())

    client_socket.close()


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 1234))
server_socket.listen()
print("Server started")

while True:
    client_socket, client_address = server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()

```

### Пояснение:
В рамках работы было реализовано 2 основных функции: 
1. Генерируем HTML-страницу, которая заполняется данными из словаря. Словарь является хранилищем данных и содержит в себе ключ в виде дисциплины и значение в виде оценок
2. Обработка клиента, в рамках которой идет обработка запроса (POST и GET), в зависимости от результата выстраивается работа. Если это GET-запрос, то генерируется HTML-страница, а если POST, то идет обработка введенных данных о пользвоателя и добавление их в словарь