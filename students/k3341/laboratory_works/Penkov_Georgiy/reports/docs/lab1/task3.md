# Лабораторная 1, Задание 3
## Условие
Реализовать серверную часть приложения. Клиент подключается к серверу, и в ответ получает HTTP-сообщение, содержащее HTML-страницу, которая сервер подгружает из файла index.html.
### Требования:
- Обязательно использовать библиотеку socket.
## Решение
`index.html`
```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My website</title>
</head>
<body>
    <h1>Hello, client!</h1>
    <p>This is the main page of my website :^)</p>
</body>
</html>
```

`server.py`
```
import socket
import os


def get_index_page():
    current_path = os.path.dirname(__file__)
    file_path = os.path.join(current_path, "index.html")
    file = open(file_path)
    content = file.read()
    file.close()
    return content


SERVER_ADDRESS = ("localhost", 1234)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(SERVER_ADDRESS)

server_socket.listen(0)
print(f"Listening on {SERVER_ADDRESS}")

while True:
    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address}")

    request = client_socket.recv(1024).decode()
    if not request:
        break
    print(f"Received: {request}")

    content = get_index_page()

    response = "HTTP/1.0 200 OK\n\n" + content
    client_socket.sendall(response.encode())
    client_socket.close()

server_socket.close()
print("Server closed.")

```
