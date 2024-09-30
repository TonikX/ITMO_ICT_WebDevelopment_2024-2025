## Задание 3:
Реализовать серверную часть приложения. 
Клиент подключается к серверу, и в ответ получает HTTP-сообщение, 
содержащее HTML-страницу, которая сервер подгружает из файла index.html.

### Стэк реализации:
- Язык - Python
- Библиотеки - socket
- Протокол - TCP

### Запуск программ:
Сервер:
```bash
    python server.py
```
Клиент:
```bash
    python client.py
```

### Листинг кода:

Сервер:
```python
import socket

HOST = 'localhost'
PORT = 8080
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))

server_socket.listen(5)
print(f"HTTP сервер запущен на {HOST}:{PORT}...")

while True:
    client_connection, client_address = server_socket.accept()

    print(f'Подключение от {client_address}')
    request = client_connection.recv(1024).decode()

    print(f'Запрос клиента:\n{request}')
    with open('index.html', 'r', encoding='utf-8') as file:
        html_content = file.read()

    http_response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html; charset=UTF-8\r\n"
            f"Content-Length: {len(html_content.encode('utf-8'))}\r\n"
            "Connection: close\r\n"
            "\r\n" + html_content
    )

    client_connection.sendall(http_response.encode())

    client_connection.close()
```

Листинг html файла index.html:
```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Простой сервер.</title>
</head>
<body>
    <h1>Привет! Это простая HTML-страница.</h1>
</body>
</html>
```

Клиент:
```python
import socket

server_host = 'localhost'
server_port = 8080

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_host, server_port))

http_request = "GET / HTTP/1.1\r\nHost: localhost\r\nConnection: close\r\n\r\n"
client_socket.sendall(http_request.encode())

response = b""
while True:
    data = client_socket.recv(1024)
    if not data:
        break
    response += data

client_socket.close()

http_response = response.decode('utf-8')
print("Ответ сервера:")
print(http_response)

html_start = http_response.find("\r\n\r\n") + 4
html_content = http_response[html_start:]

client_socket.close()
```