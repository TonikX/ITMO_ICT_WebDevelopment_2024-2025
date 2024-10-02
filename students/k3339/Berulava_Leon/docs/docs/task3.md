# Задание 3

Реализовать серверную часть приложения. Клиент подключается к серверу, и в ответ получает HTTP-сообщение, содержащее HTML-страницу, которая сервер подгружает из файла index.html.

Обязательно использовать библиотеку socket.
## Код
Серверная часть
```python
import socket

# Чтение содержимого HTML-файла
with open('index.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Создание HTTP-ответа
response = f"""\
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: {len(html_content)}

{html_content}
"""


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


server_socket.bind(('localhost', 8080))
```
Клиентская часть

```python
import socket

# Создаем TCP-сокет
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Подключаемся к серверу (например, localhost и порт 8080)
server_address = ('localhost', 8080)
client_socket.connect(server_address)

# Формируем простой HTTP-запрос
http_request = "GET / HTTP/1.1\r\nHost: localhost\r\n\r\n"

# Отправляем запрос на сервер
client_socket.sendall(http_request.encode('utf-8'))

# Получаем ответ от сервера
response = client_socket.recv(4096).decode('utf-8')

# Выводим ответ
print(response)

# Закрываем соединение
client_socket.close()
```