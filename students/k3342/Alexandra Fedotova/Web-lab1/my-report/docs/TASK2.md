# **Задание 2**

Реализовать клиентскую и серверную часть приложения. Клиент запрашивает выполнение математической операции, параметры которой вводятся с клавиатуры. Сервер обрабатывает данные и возвращает результат клиенту.

## **Поиск площади параллелограмма**.
Площадь параллелограмма вычисляется по формуле S = a * h, где a - основание фигуры, h - высота фигуры.

### **Требования**:
- Обязательно использовать библиотеку `socket`.
- Реализовать с помощью протокола TCP.

## **Серверная часть:**

```python
import socket

# Настройки сервера
SERVER_IP = 'localhost'  # Привязка к localhost
SERVER_PORT = 8080
BUFFER_SIZE = 1024

# Создаем TCP сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Разрешить повторное использование адреса
server_socket.bind((SERVER_IP, SERVER_PORT))

# Слушаем входящие подключения
server_socket.listen(1)
print(f"Сервер запущен на {SERVER_IP}:{SERVER_PORT} и ожидает подключений...")

while True:
    # Принимаем соединение от клиента
    client_socket, client_address = server_socket.accept()
    print(f"Подключен клиент с адресом {client_address}")

    try:
        # Получаем сообщение с параметрами (основание и высота)
        data = client_socket.recv(BUFFER_SIZE).decode()
        print(f"Получены данные от клиента: {data}")

        # Разбиваем параметры и вычисляем площадь параллелограмма
        base, height = map(float, data.split(","))
        area = base * height
        print(f"Вычисленная площадь параллелограмма: {area}")

        # Отправляем результат обратно клиенту
        client_socket.send(str(area).encode())
    except Exception as e:
        print(f"Ошибка: {e}")
        client_socket.send(f"Ошибка обработки данных: {e}".encode())

    # Закрываем соединение с клиентом
    client_socket.close()
```
## **Клиентская часть**:

```python
import socket

# Настройки клиента
SERVER_IP = 'localhost'  # Соединение с сервером по localhost
SERVER_PORT = 8080
BUFFER_SIZE = 1024

# Создаем TCP сокет
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Подключаемся к серверу
client_socket.connect((SERVER_IP, SERVER_PORT))

# Ввод параметров с клавиатуры
base = input("Введите основание параллелограмма: ")
height = input("Введите высоту параллелограмма: ")

# Отправляем параметры на сервер
client_socket.send(f"{base},{height}".encode())

# Получаем и выводим результат от сервера
result = client_socket.recv(BUFFER_SIZE).decode()
print(f"Результат от сервера: Площадь параллелограмма = {result}")

# Закрываем сокет
client_socket.close()
```