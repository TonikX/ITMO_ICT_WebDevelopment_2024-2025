Задание: Реализовать серверную часть приложения. Клиент подключается к серверу, и в ответ получает HTTP-сообщение, содержащее HTML-страницу, которая сервер подгружает из файла index.html.

Листинг кода:

```
import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("127.0.0.1", 9090))
server_socket.listen(10)
server_socket.settimeout(1)

try:
    while True:
        try:
            client_socket, client_address = server_socket.accept()

            with open("index.html", encoding="utf-8") as file:
                index_html = file.read().encode()

            response_headers = (
                "HTTP/1.1 200 OK\n"
                "Content-Type: text/html\n"
                f"Content-Length: {len(index_html)}\n"
                "Connection: close\n\n"
            ).encode()

            client_socket.sendall(response_headers + index_html)

        except socket.timeout:
            pass

except KeyboardInterrupt:
    server_socket.close()
```
Объяснение: 

Берем под основу программу из предыдущего задания. 

1. С помощью with open() чтение из index.html файла
2. К содержимому HTML-файла добавляем к запросу заголовки:
3. Connection: close: даёт клиенту понять, что соединение нужно остановить.

Для проверки работы html-файла можно перейти по ссылке:
http://127.0.0.1:9090/