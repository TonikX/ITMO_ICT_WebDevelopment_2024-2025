# Задание 2

## Суть задания

Реализовать клиентскую и серверную часть приложения. Клиент запрашивает выполнение математической операции, параметры которой вводятся с клавиатуры. Сервер обрабатывает данные и возвращает результат клиенту.

**Варианты операций**:
1. Теорема Пифагора
2. Решение квадратного уравнения
3. Поиск площади трапеции
4. Поиск площади параллелограмма

**Требования**:
- Обязательно использовать библиотеку socket
- Реализовать с помощью протокола TCP


### Клиент

Клиент запрашивает у пользователя значения катетов, отправляет их на сервер и получает гипотенузу. Код клиента представлен ниже:

```python
import socket

HOST = socket.gethostbyname(socket.gethostname())
PORT = 1313
BUFFER_SIZE = 1024

def get_legs():
    while True:
        try:
            leg_1, leg_2 = map(float, input("Введите значения катетов через пробел\n").split())
            return leg_1, leg_2
        except ValueError:
            print("Неправильно введены значения катетов. Пожалуйста, введите числовые значения.")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

leg_1, leg_2 = get_legs()
client.sendall(f"{leg_1}, {leg_2}".encode())

print(f'Гипотенуза = {client.recv(BUFFER_SIZE).decode()}')
```

### Сервер

Сервер принимает значения катетов от клиента, вычисляет гипотенузу и отправляет результат обратно. Код сервера представлен ниже:

```python
import socket
import math

HOST = socket.gethostbyname(socket.gethostname())
PORT = 1313
BUFFER_SIZE = 1024

def find_hypotenuse(leg_1, leg_2):
    hypotenuse = math.sqrt(float(leg_1) ** 2 + float(leg_2) ** 2)
    return hypotenuse

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen(5)

while True:
    client, addr = server.accept()
    data = client.recv(BUFFER_SIZE).decode()
    leg_1, leg_2 = data.split(',')
    answer = find_hypotenuse(leg_1, leg_2)
    client.send(str(answer).encode())
```