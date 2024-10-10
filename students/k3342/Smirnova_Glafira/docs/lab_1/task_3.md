### Задание

Реализовать серверную часть приложения. Клиент подключается к серверу, и в ответ получает HTTP-сообщение, содержащее HTML-страницу, которая сервер подгружает из файла index.html.
### `server.py`

```python
import socket


def load_html():
    try:
        with open('index.html', 'r', encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return "<html><body><h1>404 Not Found</h1></body></html>"


def handle_client(client_socket):
    try:
        html_content = load_html()

        response = f"HTTP/1.1 200 OK\nContent-Type: text/html\n\n{html_content}"

        client_socket.sendall(response.encode())

    finally:
        client_socket.close()


def start_server(host='127.0.0.1', port=8080):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()
    print(f"Сервер запущен на {host}:{port}")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            handle_client(client_socket)
    finally:
        server_socket.close()


if __name__ == "__main__":
    start_server()

```

Сервер создает сокет, работающий по протоколу TCP и ожидает запрос от клиента. При получении запроса сервер считывает данные из файла index.html. Формируется response, состоящий из заголовков и тела ответа, который впоследствии возвращается клиенту в виду HTML-страницы.

Ссылка на хост: http://127.0.0.1:8080/