Задание: Реализовать серверную часть приложения. Клиент подключается к серверу, и в ответ получает HTTP-сообщение, содержащее HTML-страницу, которая сервер подгружает из файла index.html.

Листинг кода:
```
import socket


def connection():
    host = '127.0.0.1'
    port = 8080

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print('Сервер запущен...')

    while True:
        client_conn, client_addr = server_socket.accept()

        with open('index.html', 'r') as f:
            content = f.read()

        response = f"HTTP/1.1 200 OK\nContent-Type: text/html\nContent-Length: {len(content)}\n\n{content}"
        client_conn.sendall(response.encode())

        client_conn.close()


if __name__ == "__main__":
    connection()
```

Для проверки работоспособности переходим по
```
http://127.0.0.1:8080/
```