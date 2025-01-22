# Отчет по Заданию 2: TCP Математические операции

## Описание задания
Реализовать клиент и сервер, которые позволяют клиенту запросить выполнение математической операции. Сервер обрабатывает запрос и возвращает результат.

## Реализация

### Сервер:
```
import socket


def parallelogram_area(base, height):
    return base * height


# Настройка TCP-сервера
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 2020))
server_socket.listen(1)

print("Сервер ожидает подключения...")

while True:
    conn, addr = server_socket.accept()
    print(f"Подключен клиент: {addr}")

    data = conn.recv(1024).decode()
    base, height = map(float, data.split())

    result = parallelogram_area(base, height)
    conn.sendall(f"Площадь параллелограмма: {result}".encode())

    conn.close()
```
### Клиент:
```
import socket

# Настройка TCP-клиента
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 2020))

# Ввод параметров
base = input("Введите длину основания: ")
height = input("Введите высоту: ")
client_socket.sendall(f"{base} {height}".encode())

# Получение результата
result = client_socket.recv(1024).decode()
print(result)

client_socket.close()
```
## Вывод:
Реализовано успешное выполнение математической операции на сервере по запросу клиента.