## **Задание:**

Реализовать серверную часть приложения. Клиент подключается к серверу, и в ответ получает HTTP-сообщение, содержащее HTML-страницу, которую сервер подгружает из файла `index.html`.

## **Решение:**

Серверная часть:

   - Сервер создает TCP-сокет и ждет подключения клиентов.
   - Принимает HTTP-запрос, определяет метод и URL.
   - Если запрос — GET, отправляет содержимое HTML-страницы из файла `index.html`.
   - Формирует корректный HTTP-ответ с содержимым HTML и отправляет клиенту.

## **Код:**

server.py
```python
import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8080))
server_socket.listen(1)

while True:
    client_connection, client_address = server_socket.accept()
    request = client_connection.recv(1024).decode()

    html_content = open('index.html', 'r', encoding='utf-8').read()

    http_response = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html; charset=UTF-8\r\n"
        f"Content-Length: {len(html_content.encode())}\r\n"
        "Connection: close\r\n"
        "\r\n"
        + html_content
    )

    client_connection.sendall(http_response.encode())
    client_connection.close()
```