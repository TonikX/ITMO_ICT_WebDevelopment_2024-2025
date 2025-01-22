import socket
import os

# Настройка сервера
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 3030))
server_socket.listen(1)

print("Сервер ожидает подключения...")

while True:
    conn, addr = server_socket.accept()
    print(f"Подключен клиент: {addr}")

    # Чтение HTML-файла
    with open('index.html', 'r') as file:
        html_content = file.read()

    # Формирование HTTP-ответа
    response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n{html_content}"

    conn.sendall(response.encode())
    conn.close()
