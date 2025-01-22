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
