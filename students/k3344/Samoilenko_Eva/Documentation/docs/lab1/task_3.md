### Задание 3:

Реализовать серверную часть приложения. Клиент подключается к серверу, и в ответ получает HTTP-сообщение, содержащее HTML-страницу, которая сервер подгружает из файла index.html.

Требования:

- Обязательно использовать библиотеку socket.


### Ход работы:

#### server.py

```
import socket

serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv_address = ('localhost', 8080)
serv_sock.bind(serv_address)
serv_sock.listen(1)

while True:
    conn, cl_address = serv_sock.accept()
    data = conn.recv(1024).decode()

    with open('index.html', 'r') as file:
        html_content = file.read()

    message = f"HTTP/1.1 200 OK\r\n" \
              f"Content-Type: text/html\r\n" \
              f"Content-Length: {len(html_content)}\r\n" \
              f"\r\n" \
              f"{html_content}"

    conn.sendall(message.encode())

    conn.close()

```

После написания простенького HTML-файла прописываем серверную часть приложения, которая 
осуществляет работу нашего сайта.

Чтобы убедиться в работе сайта, переходим по заданному адресу `http://localhost:8080`