# Задание 3

## Суть задания

Реализовать серверную часть приложения. Клиент подключается к серверу, и в ответ получает HTTP-сообщение, содержащее HTML-страницу, которая сервер подгружает из файла index.html.

**Требования**:
- Обязательно использовать библиотеку socket

## Код программы

### Сервер

```python
import socket

HOST = '0.0.0.0'  
PORT = 1313       

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

while True:
    client, addr = server.accept()
    print(f'Connection from {addr}')

    request = client.recv(1024).decode()
    print(f'Client request:\n{request}')

    with open('index.html', 'r') as file:
        content = file.read()

    response = 'HTTP/1.0 200 OK\n\n' + content

    client.sendall(response.encode())

server.close()
```

### html-страница
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OKTIOKTIOKTI</title>
</head>
<body>
    <h1>OKTIOKTIOKTI</h1>
    <p>OKTIOKTIOKTI</p>
</body>
</html>
```