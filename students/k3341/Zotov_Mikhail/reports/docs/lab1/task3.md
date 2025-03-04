# Задание 3<br><br>
### Условие
Реализовать серверную часть приложения. Клиент подключается к серверу, и в ответ получает HTTP-сообщение, содержащее HTML-страницу, которая сервер подгружает из файла `index.html`.

#### Требования:
- Обязательно использовать библиотеку `socket`.

---
### Код
#### Сервер
```python
import socket


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('localhost', 2024))
sock.listen(0)
print("Server listening on port 2024")

with open("index.html", encoding='utf-8') as file:
    page = file.read()

while True:
    client_socket, client_address = sock.accept()
    print("Got connection from", client_address)

    client_socket.sendall(f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n{page}".encode())
```