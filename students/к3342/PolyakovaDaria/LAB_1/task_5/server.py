import socket
from urllib.parse import parse_qs

# Хранилище для оценок
grades = []

# Функция для формирования HTML-страницы с формой и списком оценок
def generate_html():
    html = """
    <html>
    <head>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 20px;
            }
            h1 {
                color: #333;
            }
            form {
                background: white;
                padding: 20px;
                border-radius: 5px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            }
            input[type="text"] {
                width: 100%;
                padding: 10px;
                margin: 10px 0;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            input[type="submit"] {
                background-color: #5cb85c;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
            }
            input[type="submit"]:hover {
                background-color: #4cae4c;
            }
            ul {
                list-style-type: none;
                padding: 0;
            }
            li {
                background: white;
                margin: 5px 0;
                padding: 10px;
                border-radius: 4px;
                box-shadow: 0 1px 5px rgba(0, 0, 0, 0.1);
            }
        </style>
    </head>
    <body>
        <h1>Введите дисциплину и оценку</h1>
        <form method="POST" action="/">
            Дисциплина: <input type="text" name="subject"><br>
            Оценка: <input type="text" name="grade"><br>
            <input type="submit" value="Отправить">
        </form>
    """

    if grades:
        html += "<h2>Список оценок:</h2><ul>"
        for entry in grades:
            html += f"<li>{entry['subject']}: {entry['grade']}</li>"
        html += "</ul>"

    html += "</body></html>"
    return html

# Создание сокета
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8080))
server_socket.listen(1)

print("Сервер запущен на http://localhost:8080")

while True:
    client_socket, addr = server_socket.accept()
    request = client_socket.recv(1024).decode()
    print(request)

    # Получение метода запроса и пути
    request_line = request.splitlines()[0]
    method, path, _ = request_line.split()

    if method == 'GET':
        # Формируем ответ для GET-запроса
        response_body = generate_html()
        response = 'HTTP/1.1 200 OK\nContent-Type: text/html; charset=utf-8\n\n' + response_body

    elif method == 'POST':
        # Получение данных из POST-запроса
        body = request.split('\r\n\r\n')[1]
        data = parse_qs(body)

        # Записываем дисциплину и оценку
        subject = data.get('subject', [''])[0]
        grade = data.get('grade', [''])[0]
        if subject and grade:
            grades.append({'subject': subject, 'grade': grade})

        # Формируем ответ после обработки POST-запроса
        response_body = generate_html()
        response = 'HTTP/1.1 200 OK\nContent-Type: text/html; charset=utf-8\n\n' + response_body

    else:
        response = 'HTTP/1.1 405 Method Not Allowed\n\n'

    # Отправка ответа клиенту
    client_socket.sendall(response.encode('utf-8'))
    client_socket.close()