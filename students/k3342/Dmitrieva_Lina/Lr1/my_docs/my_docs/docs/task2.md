# Задание 2: 

## Описание задачи

Реализовать клиентскую и серверную часть приложения. Клиент запрашивает выполнение математической операции(решение квадратного уравнения), параметры которой вводятся с клавиатуры. Сервер обрабатывает данные и возвращает результат клиенту.

## Код сервера
```python
import socket
import math

def solve_quadratic(a, b, c):
    """Решение квадратного уравнения."""
    discriminant = b**2 - 4*a*c
    if discriminant > 0:
        # Два действительных корня
        x1 = (-b + math.sqrt(discriminant)) / (2 * a)
        x2 = (-b - math.sqrt(discriminant)) / (2 * a)
        return f"Два корня: x1 = {x1}, x2 = {x2}"
    elif discriminant == 0:
        # Один действительный корень
        x = -b / (2 * a)
        return f"Один корень: x = {x}"
    else:
        # Действительных корней нет
        return "Корней нет (дискриминант отрицательный)"

server_address = ('localhost', 8080)
#Создание TCP-сокета
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Привязываем сокет к адресу и порту
sock.bind(server_address)

#Ожидаем подключения клиента
sock.listen(1)
print('Сервер запущен и ожидает подключения клиента...')

while True:
#Принятие соединения
    connection, client_address = sock.accept()
    try:
        print(f'Подключен клиент: {client_address}')

#Получаем данные от клиента
        data = connection.recv(1024).decode()
        print(f'Получены данные: {data}')

        if data:
        #Разбираем коэффициенты квадратного уравнения
            a, b, c = map(float, data.split(','))
            
            #Решаем квадратное уравнение
            result = solve_quadratic(a, b, c)
            
            #Отправляем результат обратно клиенту
            connection.sendall(result.encode())
            print(f'Результат отправлен клиенту: {result}')
    finally:
        connection.close()
```
## Код клиента
```python
import socket

#Создание TCP-сокета
server_address = ('localhost', 8080)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    #Подключение к серверу
    sock.connect(server_address)
    
    #Ввод коэффициентов квадратного уравнения с клавиатуры
    a = input("Введите коэффициент a: ")
    b = input("Введите коэффициент b: ")
    c = input("Введите коэффициент c: ")
    
    #Отправка данных на сервер
    message = f'{a},{b},{c}'
    sock.sendall(message.encode())
    print(f'Отправлены данные: a={a}, b={b}, c={c}')
    
    #Ожидание и получение результата от сервера
    data = sock.recv(1024)
    print(f'Получен результат от сервера: {data.decode()}')
    
finally:
    sock.close()
```