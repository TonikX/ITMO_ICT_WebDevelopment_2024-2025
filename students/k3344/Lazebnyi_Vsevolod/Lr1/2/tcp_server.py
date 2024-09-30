import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("localhost", 8080))
server_socket.listen()
print("Сервер запущен на порту 8080...")
client_connection, client_address = server_socket.accept()
with client_connection:
    client_message = client_connection.recv(1024).decode()
    a, b, c = client_message.split(',')
    solve = (float(a) + float(b))*float(c)/2
    client_connection.sendall(str(solve).encode())