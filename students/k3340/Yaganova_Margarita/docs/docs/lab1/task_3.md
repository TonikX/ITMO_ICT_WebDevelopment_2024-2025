### Задание 3:

Реализовать серверную часть приложения. Клиент подключается к серверу, и в ответ получает HTTP-сообщение, содержащее HTML-страницу, которая сервер подгружает из файла index.html.

Требования:

- Обязательно использовать библиотеку socket.


### Ход работы:

#### server.py

```
import socket


def start_http_server():
    host = 'localhost'
    port = 8080

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind((host, port))

    server_socket.listen(5)
    print(f"Server listening on {host}:{port}...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")

        request_data = client_socket.recv(1024).decode('utf-8')
        print(f"Request received:\n{request_data}")

        with open("index.html", "r") as file:
            html_content = file.read()

        http_response = (
            "HTTP/1.1 200 OK\n"
            "Content-Type: text/html\n"
            "Content-Length: {}\n"
            "Connection: close\n\n"
            "{}".format(len(html_content), html_content)
        )

        client_socket.sendall(http_response.encode('utf-8'))

        client_socket.close()
        print(f"Connection with {client_address} closed")


if __name__ == "__main__":
    start_http_server()
```

Создаем HTML-файл для сатайта, затем пишем серверную часть приложения, которая 
осуществляет работу нашего сайта.

Чтобы убедиться в работе сайта, переходим по заданному адресу `http://localhost:8080`
