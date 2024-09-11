# Задание 3: Простой веб-сервер

Реализовать серверную часть приложения. Клиент подключается к серверу, и в ответ получает HTTP-сообщение, содержащее HTML-страницу, которая сервер подгружает из файла index.html.  

Требования:  
- Обязательно использовать библиотеку `socket`.

## Файлы
- `server.py`: Реализация сервера
```python
import socket

buffer_size = 1024
host = 'localhost'
port = 8000
server_address = (host, port)

def load_html_file():
    try:
        with open('index.html', 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return "<h1>Файл index.html не найден!</h1>"

def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(server_address)
    server_socket.listen(5)  # waiting for 5 clients simultaneously

    print(f"Server is running on {host}:{port}")

    while True:
        client_connection, client_address = server_socket.accept()
        print(f"Client connection: {client_address}")

        request = client_connection.recv(buffer_size).decode('utf-8')
        print(f"Client request:\n{request}")

        response_body = load_html_file()

        response = 'HTTP/1.1 200 OK\r\n'
        response += 'Content-Type: text/html\r\n'
        response += 'Content-Length: ' + str(len(response_body)) + '\r\n'
        response += '\r\n'
        response += response_body

        client_connection.sendall(response.encode('utf-8'))
    client_connection.close()

if __name__ == "__main__":
    server()

```
