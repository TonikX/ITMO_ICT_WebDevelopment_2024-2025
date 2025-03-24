# Задание 2

Реализовать клиентскую и серверную часть приложения. Клиент запрашивает выполнение математической операции, параметры которой вводятся с клавиатуры. Сервер обрабатывает данные и возвращает результат клиенту.

Математическая операция: Площадь параллелограмма.

- Язык реализации: Python
- Протокол: TCP
- Используемые библиотеки: socket

## Реализация
client.py
```python
import socket

# Создаем сокет
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Подключаемся к серверу
client_socket.connect(('localhost', 8080))

# Запрашиваем у пользователя параметры для вычисления площади
a = input("Введите основание параллелограмма: ")
h = input("Введите высоту параллелограмма: ")

# Отправляем сообщение серверу
message = f"{a} {h}"
client_socket.sendall(message.encode())

# Получаем ответ от сервера
response = client_socket.recv(1024)
print(f'Ответ от сервера: {response.decode()}')

# Закрываем соединение
client_socket.close()
```
server.py
```python
import socket

# Создаем сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Привязываем сокет к адресу и порту
server_socket.bind(('localhost', 8080))

# Начинаем слушать входящие подключения (ожидание клиентов)
server_socket.listen(1)
print("Сервер запущен на порту 8080...")

while True:
    # Принимаем соединение от клиента
    client_connection, client_address = server_socket.accept()
    print(f'Подключение от {client_address}')

    # Получаем сообщение от клиента
    request = client_connection.recv(1024).decode()
    print(f'Запрос от клиента: {request}')

    # Высчитываем площадь параллелограмма
    a, h = str(request).split(' ')
    response = str(int(a) * int(h))

    # Отправляем ответ клиенту
    client_connection.sendall(response.encode())

    # Закрываем соединение
    client_connection.close()
```
## Запуск
- Запустите сервер:
```bash
python server.py
```
- Запустите клиента:
```bash
python client.py
```