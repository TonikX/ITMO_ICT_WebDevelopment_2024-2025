import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(('localhost', 8080))

server_socket.listen(1)
print("Сервер запущен на порту 8080...")

while True:
    client_connection, client_address = server_socket.accept()
    print(f'Подключение от {client_address}')

    data = client_connection.recv(1024).decode()
    if not data:
        break
    a, b, h = map(int, data.split())
    result = (a+b)*h*0.5
    client_connection.send(str(result).encode())
    print(f'Отправлен результат: {result}')

    client_connection.close()