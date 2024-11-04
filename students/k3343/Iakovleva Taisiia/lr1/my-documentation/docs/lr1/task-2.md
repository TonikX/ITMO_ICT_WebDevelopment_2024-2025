# Задние 2

## Текст задания

Реализовать клиентскую и серверную часть приложения. Клиент запрашивает выполнение математической операции - теоремы Пифагора, параметры которой вводятся с клавиатуры. Сервер обрабатывает данные и возвращает результат клиенту.

## Требования

- Обязательно использовать библиотеку socket.
- Реализовать с помощью протокола TCP.

## Запуск

1. Запуск сервера

```python
python3 server.py
```

2. Запуск клиента

```python
python3 client.py
```

## Код

### client.py

```python
import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect(('localhost', 8080))

a = input("Введите длину стороны a: ")
b = input("Введите длину стороны b: ")

client_socket.sendall(f"{a} {b}".encode())

response = client_socket.recv(1024)
print(f'Ответ от сервера: {response.decode()}')

client_socket.close()
```

### server.py

```python
import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(('localhost', 8080))

server_socket.listen(1)
print("Сервер запущен на порту 8080...")

while True:

    client_connection, client_address = server_socket.accept()
    print(f'Подключение от {client_address}')

    request = client_connection.recv(1024).decode()
    print(f'Запрос от клиента: {request}')

    a, b = map(float, request.split())

    c = (a ** 2 + b ** 2) ** 0.5
    response = f"Гипотенуза: {c:.2f}"
    client_connection.sendall(response.encode())

    client_connection.close()
```

## Описание работы кода

### Клиентская часть 

- Создается TCP-сокет, который подключается к серверу на адресе localhost и порту 8080
- Пользователь вводит значения сторон a и b, которые отправляются серверу
- Получает от сервера результат — вычисленное значение гипотенузы — и выводит его на экран
- Закрывает соединение после завершения взаимодействия

### Серверная часть 

- Создается TCP-сокет, который привязывается к адресу localhost и порту 8080 и начинает прослушивание входящих соединений
- Сервер принимает соединение, получает данные от клиента и выводит их на экран
- Выполняет расчет гипотенузы и отправляет результат обратно клиенту
- Закрывает соединение с клиентом после отправки ответа