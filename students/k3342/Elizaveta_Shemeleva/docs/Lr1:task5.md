# Отчет по Заданию 5: HTTP GET/POST сервер

## Описание задания
Создать веб-сервер, обрабатывающий GET и POST запросы, для записи и отображения информации о дисциплинах и оценках.

## Реализация

### Сервер:
```
import socket

grades = {}

def handle_request(request):
    lines = request.splitlines()
    request_line = lines[0].split()
    method = request_line[0]
    path = request_line[1]

    if method == 'POST' and path == '/submit':
        body = lines[-1]
        discipline, grade = body.split(',')
        grades[discipline] = grade
        response = 'HTTP/1.1 200 OK\r\n\r\nДанные сохранены!'
    elif method == 'GET':
        html_content = "<html><body><h1>Оценки</h1><ul>"
        for discipline, grade in grades.items():
            html_content += f"<li>{discipline}: {grade}</li>"
        html_content += "</ul></body></html>"
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n{html_content}"
    else:
        response = 'HTTP/1.1 404 NOT FOUND\r\n\r\nСтраница не найдена!'

    return response

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 5050))
server_socket.listen(1)

print("Сервер ожидает подключения...")

while True:
    conn, addr = server_socket.accept()
    request = conn.recv(1024).decode()
    print(f"Запрос от клиента: {request}")
    response = handle_request(request)
    conn.sendall(response.encode())
    conn.close()
```
## Вывод:
HTTP сервер успешно обрабатывает запросы и отображает информацию.

