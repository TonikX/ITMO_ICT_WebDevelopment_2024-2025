# Задание 5: Веб-сервер для обработки GET и POST HTTP-запросов
## Описание
Сервер обрабатывает POST-запросы для сохранения данных и GET-запросы для отображения HTML-страницы с таблицей данных.

### Серверная часть
```
import socket
import threading
from urllib.parse import parse_qs

# Словарь для хранения дисциплин и оценок
grades = {}


def handle_request(conn):
    request = conn.recv(1024).decode()
    headers = request.splitlines()
    if not headers:
        return

    # Обработка метода запроса
    method = headers[0].split()[0]
    if method == 'POST':
        # Обработка POST запроса
        content_length = int([h for h in headers if h.startswith('Content-Length:')][0].split(': ')[1])
        body = request.splitlines()[-1]
        data = parse_qs(body)
        subject = data.get('subject', [''])[0]
        grade = data.get('grade', [''])[0]
        if subject and grade:
            grades[subject] = grade
        response = 'HTTP/1.1 200 OK\n\nGrade added!'

    elif method == 'GET':
        # Обработка GET запроса - генерируем таблицу с оценками
        response_body = '''
        <html>
        <head><title>Grades</title></head>
        <body>
            <h1>Grades</h1>
            <table border="1">
                <tr><th>Subject</th><th>Grade</th></tr>
        '''

        # Добавляем строки для каждой дисциплины
        for subject, grade in grades.items():
            response_body += f'<tr><td>{subject}</td><td>{grade}</td></tr>'

        response_body += '''
            </table>
        </body>
        </html>
        '''

        response = f'HTTP/1.1 200 OK\nContent-Type: text/html\n\n{response_body}'

    else:
        response = 'HTTP/1.1 405 Method Not Allowed\n\n'

    conn.sendall(response.encode())
    conn.close()


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8082))
    server_socket.listen(5)
    print("Server running on http://localhost:8082")

    while True:
        conn, addr = server_socket.accept()
        threading.Thread(target=handle_request, args=(conn,)).start()


if __name__ == "__main__":
    start_server()
```
### Клиентская часть
```
import socket
import threading


def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode()
            if message:
                print(message)
        except:
            print("Соединение потеряно")
            sock.close()
            break

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))

threading.Thread(target=receive_messages, args=(client_socket,)).start()

while True:
    message = input()
    client_socket.send(message.encode())
```