# Отчет по Заданию 3: HTTP-сервер

## Описание задания
Реализовать сервер, который отправляет клиенту HTML-страницу через HTTP.

## Реализация

### Сервер:
```
import socket
import os

# Настройка сервера
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 3030))
server_socket.listen(1)

print("Сервер ожидает подключения...")

while True:
    conn, addr = server_socket.accept()
    print(f"Подключен клиент: {addr}")

    # Чтение HTML-файла
    with open('index.html', 'r') as file:
        html_content = file.read()

    # Формирование HTTP-ответа
    response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n{html_content}"

    conn.sendall(response.encode())
    conn.close()
```
### HTML-страница:
```
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Пример HTML-страницы</title>
</head>
<body>
    <h1>Добро пожаловать!</h1>
    <p>Это пример HTML-страницы, загруженной сервером.</p>
</body>
</html>
```
## Вывод:
HTTP-сервер успешно отправляет клиенту HTML-страницу.
