# Задание
Реализовать серверную часть приложения. Клиент подключается к серверу, и в ответ получает HTTP-сообщение, содержащее
HTML-страницу, которая сервер подгружает из файла index.html.

**Требования:**

- Обязательно использовать библиотеку socket.
 
***

# Решение

## Сервер

```python
import socket
import webbrowser
import tempfile

HOST = 'localhost'
PORT = 9090


with socket.socket() as client_socket:
    client_socket.connect((HOST, PORT))

    http_request = "GET / HTTP/1.1\r\nHost: localhost\r\nConnection: close\r\n\r\n"
    client_socket.sendall(http_request.encode('utf-8'))

    response = b""
    while True:
        part = client_socket.recv(1024)
        if not part:
            break
        response += part

    header_end = response.find(b"\r\n\r\n")
    html_content = response[header_end + 4:].decode('utf-8')

    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html') as f:
        f.write(html_content)
        temp_file_path = f.name

    webbrowser.open(f'file://{temp_file_path}')

    print(response.decode('utf-8'))

```
## Сервер

```python
import socket

HOST = 'localhost'
PORT = 9090

def main():
    sock = socket.socket()
    sock.bind((HOST, PORT))
    sock.listen(1)

    print("Server started, waiting for connection...")

    while True:
        conn, addr = sock.accept()
        print('Connected:', addr)

        request = conn.recv(1024).decode('utf-8')
        print("Received request:")
        print(request)

        try:
            with open("index.html", "r", encoding="utf-8") as file:
                html_content = file.read()
        except FileNotFoundError:
            html_content = "<h1>file index.html not found</h1>"

        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n{html_content}"
        conn.sendall(response.encode('utf-8'))

        conn.close()

if __name__ == "__main__":
    main()
```

***

# Пояснение

Создаём TCP сокет на сервере, используя адрес `127.0.0.1` и порт `9090` и устанавливаем соединение с клиентом.
Далее считываем файл index.html, формируем ответ `200 OK` и отправляем его клиенту.

Браузер отправляет HTTP GET запрос серверу и получает в ответ HTTP-сообщение, содержащее
HTML-страницу index.html.