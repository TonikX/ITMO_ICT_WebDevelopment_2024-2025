# Задание №2

## Текст задания

Реализовать клиентскую и серверную часть приложения. Клиент запрашивает выполнение математической операции, параметры которой вводятся с клавиатуры. Сервер обрабатывает данные и возвращает результат клиенту.

Варианты операций:

Теорема Пифагора.
Решение квадратного уравнения.
Поиск площади трапеции.
Поиск площади параллелограмма.
Порядок выбора варианта: Выбирается по порядковому номеру в журнале (пятый студент получает вариант 1 и т.д.).

Требования:

Обязательно использовать библиотеку socket.
Реализовать с помощью протокола TCP.

По варианту из таблицы мне надо реализовать теорему Пифагора.

## UDP Сервер

Этот код реализует TCP-сервер на Python, который принимает соединения от клиентов и вычисляет гипотенузу по теореме Пифагора. Сервер настраивает сокет для прослушивания на заданном адресе и порту. После принятия соединения он получает данные от клиента, парсит их для извлечения значений катетов `a` и `b`, вычисляет гипотенузу `c` и отправляет результат обратно клиенту. В случае ошибки возвращается сообщение об ошибке. После обработки запроса соединение с клиентом закрывается.

```python
import socket
import math

# Параметры сервера
HOST = 'localhost'
PORT = 8080

# Создаем сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Привязываем сокет к адресу и порту
server_socket.bind((HOST, PORT))

# Начинаем слушать входящие соединения
server_socket.listen(5)
print(f"Сервер запущен на {HOST}:{PORT}...")

while True:
    # Принимаем соединение от клиента
    client_connection, client_address = server_socket.accept()
    print(f'Подключение от {client_address}')

    # Получаем данные от клиента
    request = client_connection.recv(1024).decode()
    print(f'Запрос от клиента: {request}')

    # Парсим параметры для теоремы Пифагора (a и b)
    try:
        a, b = map(float, request.split())
        # Вычисляем гипотенузу
        c = math.sqrt(a ** 2 + b ** 2)
        response = f'Гипотенуза равна: {c:.2f}'
    except Exception as e:
        response = f'Ошибка: {str(e)}'

    # Отправляем ответ клиенту
    client_connection.sendall(response.encode())

    # Закрываем соединение
    client_connection.close()

```

## UDP Клиент

 Этот код реализует TCP-клиент на Python, который подключается к серверу для вычисления гипотенузы по теореме Пифагора. Клиент создает сокет и подключается к серверу на `localhost` и порту `8080`. Пользователь вводит длины катетов `a` и `b`, которые отправляются на сервер в виде запроса. Затем клиент получает и выводит ответ от сервера, после чего закрывает соединение.

```python
import socket

# Создаем сокет
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Подключаемся к серверу
client_socket.connect(('localhost', 8080))

# Вводим данные для теоремы Пифагора
a = input("Введите длину первого катета (a): ")
b = input("Введите длину второго катета (b): ")

# Формируем запрос серверу
request = f"{a} {b}"
client_socket.sendall(request.encode())

# Получаем ответ от сервера
response = client_socket.recv(1024)
print(f'Ответ от сервера: {response.decode()}')

# Закрываем соединение
client_socket.close()

```

