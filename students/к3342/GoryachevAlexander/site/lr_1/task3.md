# Задание 3

## Суть задания
Реализовать серверную часть приложения. Клиент подключается к серверу, и в ответ получает HTTP-сообщение, содержащее HTML-страницу, которая сервер подгружает из файла index.html.

### Сервер
```python
import socket


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", 8080)) 
    server_socket.listen(5)
    print("Сервер запущен")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Подключился клиент: {addr}")

        request = client_socket.recv(1024).decode()
        print(f"Получен запрос от клиента:\n{request}")

        try:
            with open("index.html", "r") as file:
                html_content = file.read()

            response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/html; charset=utf-8\r\n"
                f"Content-Length: {len(html_content)}\r\n"
                "\r\n"
                f"{html_content}"
            )
        except FileNotFoundError:
            response = (
                "HTTP/1.1 404 Not Found\r\n"
                "Content-Type: text/plain; charset=utf-8\r\n"
                "Content-Length: 13\r\n"
                "\r\n"
                "404 Not Found"
            )

        client_socket.sendall(response.encode())
        client_socket.close()


if __name__ == "__main__":
    main()
```
### HTML документ
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Hello there</title>
</head>
<body>
    <h1>That is an HTML</h1>
</body>
</html>

```