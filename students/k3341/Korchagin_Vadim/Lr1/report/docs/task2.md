# Вычисление по теореме Пифагора через TCP

## Условие

**Задача**: Реализовать клиентскую и серверную часть приложения, где клиент запрашивает выполнение математической операции. Клиент отправляет два числа на сервер, который вычисляет гипотенузу по теореме Пифагора и возвращает результат клиенту.

## Решение

Здесь используется более надежный протокол TCP, который гарантирует доставку данных в нужном порядке.

### Сервер (`server.py`)

* **Создание сокета**: Сервер создает TCP-сокет, привязывает его к имени хоста и порту `1236`, и ожидает подключения.
* **Получение данных**: Когда клиент подключается, сервер получает два числа, отправленные клиентом. После этого он вычисляет гипотенузу с использованием теоремы Пифагора.
* **Отправка результата**: После вычисления сервер отправляет результат клиенту.

### Клиент (`client.py`)

* **Подключение к серверу**: Клиент подключается к серверу на том же хосте и порту (`1236`).
* **Отправка чисел**: Клиент запрашивает у пользователя два числа и отправляет их на сервер.
* **Получение ответа**: После отправки чисел клиент получает результат вычислений от сервера и выводит его.

## Код

`server.py`
```python
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 1236))
s.listen(5)
message_recevied = []
message_count = 0


def pif(a, b):
    return float((a ** 2 + b ** 2) ** 0.5)


clientsocket, address = s.accept()

while True:
    try:
        data = clientsocket.recv(1024)
        if data:
            udata = data.decode('utf-8')
            message_count += 1
            message_recevied.append(udata)
            if message_count % 2 == 0:
                clientsocket.send(f"{pif(int(message_recevied[-1]), int(message_recevied[-2]))}".encode('utf-8'))
    except KeyboardInterrupt:
        s.close()
```

`client.py`
```python
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 1236))


a = input("Enter the first number: ")
b = input("Enter the second number: ")
nums = [a, b]
for num in nums:
    s.send(num.encode('utf-8'))

msg = s.recv(1024)
umsg = msg.decode('utf-8')
print(umsg)
s.close()
```