# Задание 3

Реализовать серверную часть приложения. Клиент подключается к серверу, и в ответ получает HTTP-сообщение, содержащее HTML-страницу, которая сервер подгружает из файла index.html.

## Реализация
В этом задании реализуется HTTP-сервер на Python, который обслуживает запросы от клиентов (то есть браузера) и возвращает HTML-страницу из файла `index.html`. Сервер использует библиотеку `socket` для создания сокета, который прослушивает входящие подключения на заданном хосте и порту. При получении запроса от клиента сервер читает содержимое HTML-файла и формирует HTTP-ответ (страница приветствия), отправляя его клиенту.
### Сервер
```python
import socket

HOST = 'localhost'
PORT = 8080

html_file = 'index.html'


def create_http_response(html_content):
    response = 'HTTP/1.1 200 OK\r\n'
    response += 'Content-Type: text/html\r\n'
    response += 'Content-Length: {}\r\n'.format(len(html_content))
    response += 'Connection: close\r\n'
    response += '\r\n'
    response += html_content
    return response


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)
print(f"Сервер запущен на {HOST}:{PORT}...")

while True:
    client_connection, client_address = server_socket.accept()
    print(f'Подключение от {client_address}')

    request = client_connection.recv(1024).decode()
    print(f'Запрос от клиента: {request}')

    try:
        with open(html_file, 'r') as file:
            html_content = file.read()

        http_response = create_http_response(html_content)
    except FileNotFoundError:
        http_response = 'HTTP/1.1 404 NOT FOUND\r\n'
        http_response += 'Content-Type: text/html\r\n'
        http_response += '\r\n'
        http_response += '<html><body><h1>404 Not Found</h1></body></html>'

    client_connection.sendall(http_response.encode())
    client_connection.close()


```
### Файл index.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Simple HTTP-server</title>
</head>
<body>
    <h1>Hello! This is a simple html-page.</h1>
    <p>This server is written on Python and works through sockets.</p>
</body>
</html>

```