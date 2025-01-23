# Задание 3

## Текст задания

Реализовать серверную часть приложения. Клиент подключается к серверу, и в ответ получает HTTP-сообщение, содержащее HTML-страницу, которая сервер подгружает из файла index.html.

## Требования

- Обязательно использовать библиотеку socket.

## Запуск

1. Запуск сервера

```python
python3 server.py
```

2. Запуск клиента

По  ссылке - http://127.0.0.1:8080/ - будет отображаться странца из index.html

## Код

### index.html

```html
<!DOCTYPE html>
<html>
<head>
    <title>Простой сервер на Python</title>
</head>
<body>
    <h1>Привет! Task-3.</h1>
</body>
</html>
```

### server.py

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

    with open('index.html', 'r') as file:
        html_content = file.read()
    
    http_response = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html; charset=UTF-8\r\n"
        f"Content-Length: {len(html_content)}\r\n"
        "Connection: close\r\n"
        "\r\n"
        + html_content
    )

    client_connection.sendall(http_response.encode())

    client_connection.close()
```

## Описание работы кода

- Создается TCP-сокет для прослушивания входящих соединений на localhost и порту 8080
- При подключении клиент отправляет HTTP-запрос, который сервер принимает и выводит в консоль для анализа
- Сервер открывает index.html, загружает его содержимое и формирует HTTP-ответ с кодом 200 OK
- Сформированный HTTP-ответ с HTML-контентом отправляется клиенту
- После отправки ответа соединение с клиентом закрывается