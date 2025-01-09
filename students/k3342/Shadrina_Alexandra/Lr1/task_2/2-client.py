import socket


def get_params():
    a = float(input("Длина первого основания (a): "))
    b = float(input("Длина второго основания (b): "))
    h = float(input("Высота (h): "))
    return a, b, h


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 8080))
a, b, h = get_params()

message = f'{a},{b},{h}'
client_socket.sendall(message.encode())

response = client_socket.recv(1024).decode()

if response:
    print(f'Ответ от сервера: {response}')
else:
    print('Ошибка: нет ответа от сервера')

client_socket.close()
