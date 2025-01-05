# Вариант 1
import socket
import math

# Создаем TCP сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Привязываем сокет к адресу и порту
server_socket.bind(('localhost', 8080))

# Начинаем слушать входящие подключения (ожидание клиентов)
server_socket.listen(1)
print("Server starts on port 8080...")

while True:
    # Принимаем соединение от клиента
    client_connection, client_address = server_socket.accept()
    print(f'Connection from {client_address}')

    # Получаем данные от клиента
    data = client_connection.recv(1024).decode()
    if not data:
        break

    # Получаем катеты
    cat1, cat2 = map(float, data.split(','))

    # Вычисляем гипотенузу по теореме Пифагора
    hyp = math.sqrt(cat1**2 + cat2**2)

    # Отправляем результат клиенту
    response = f'Hypotenuse is equal to {hyp:.2f}'
    client_connection.sendall(response.encode())

    # Закрываем соединение с клиентом
    client_connection.close()
