# Task 2

## Задание
Реализовать клиентскую и серверную часть приложения. Клиент запрашивает выполнение математической операции, параметры которой вводятся с клавиатуры. Сервер обрабатывает данные и возвращает результат клиенту.

**Варианты операций:**

  1. Теорема Пифагора.
  2. Решение квадратного уравнения.
  3. Поиск площади трапеции.
  4. Поиск площади параллелограмма.

**Порядок выбора варианта:** Выбирается по порядковому номеру в журнале (пятый студент получает вариант 1 и т.д.).

**Требования:**

  - Обязательно использовать библиотеку `socket`.
  - Реализовать с помощью протокола TCP.

---

## Parallelogram area calculator

You can choose specific IP address and port by changing `IP` and `PORT` variables.

Firstly run `python 2-server.py`

Then run `python 2-client.py`

Enter numbers into client's console: a, h or a, b, alpha (without commas, space as separator, alpha in degrees).

You'll see the result.

```
Parallelogram Area Calculator
Enter a, h or a, b, alpha: 10 20
Result: 200.0

Parallelogram Area Calculator
Enter a, h or a, b, alpha: 10 20 30
Result: 99.99999999999999
```

---

## Code

2-server.py:
```python
import socket
import math

IP = '127.0.0.1'
PORT = 2020

def calc(x):
  try:
    x = list(map(float, x.split()))
  except:
    return 'Wrong format'
  if len(x) == 2:
    a, h = x
    return str(a * h)
  elif len(x) == 3:
    a, b, alpha = x
    return str(a * b * math.sin(math.radians(alpha)))
  else:
    return 'Wrong format'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, PORT))
server.listen()
client, address = server.accept()
data = client.recv(1024).decode('utf-8')
client.send(calc(data).encode('utf-8'))
client.shutdown(socket.SHUT_WR)
server.close()
```

2-client.py:
```python
import socket

IP = '127.0.0.1'
PORT = 2020

print('Parallelogram Area Calculator')
x = input('Enter a, h or a, b, alpha: ')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, PORT))
client.send(x.encode('utf-8'))
data = client.recv(1024)
print('Result:', data.decode())
client.close()
```