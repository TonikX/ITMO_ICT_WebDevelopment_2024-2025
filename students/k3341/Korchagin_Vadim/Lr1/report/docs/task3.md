# Создание HTTP-сервера для отправки HTML-страницы

## Условие
**Задача**: Реализовать серверную часть приложения, в которой клиент подключается к серверу и получает HTTP-сообщение с HTML-страницей. Сервер должен загружать HTML-контент из файла `index.html` и отправлять его клиенту.

## Решение
Для решения задачи реализован простой HTTP-сервер с использованием сокетов. Сервер читает HTML-файл с диска и отправляет его в виде HTTP-ответа клиенту.

### Основные шаги:
1. **Чтение файла**: Сервер использует функцию `read_html_file` для чтения HTML-страницы из файла `index.html`.
2. **Создание HTTP-ответа**: Функция `create_http_response` создает корректное HTTP-сообщение с заголовками и телом ответа.
3. **Работа с сокетами**: Сервер принимает соединение от клиента, считывает HTML-страницу и отправляет её клиенту через сокет.

## Код

`server.py`
```python
import socket

def read_html_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        return file.read()

def create_http_response(html_content):
    response = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html; charset=utf-8\r\n"
        "Content-Length: {}\r\n"
        "Connection: close\r\n"
        "\r\n"
        "{}"
    ).format(len(html_content), html_content)
    return response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1', 1234))
s.listen(1)

while True:
    client_socket, client_address = s.accept()
    with client_socket:
        print(f"Подключен клиент: {client_address}")

        html_content = read_html_file('index.html')
        http_response = create_http_response(html_content)
        client_socket.sendall(http_response.encode('utf-8'))
```

`index.html`
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Simple HTTP Server</title>
</head>
<body>
    <h1>Welcome to the Simple HTTP Server!</h1>
    <p>This is a basic HTML page served by a Python socket server.</p>
</body>
</html>
```

`client.py`
```python
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 1234))

msg = s.recv(1024)
umsg = msg.decode('utf-8')
print(umsg)
s.close()
```