import socket

HOST = socket.gethostbyname(socket.gethostname())
PORT = 1313
BUFFER_SIZE = 1024

def get_legs():
    while True:
        try:
            leg_1, leg_2 = map(float, input("Введите значения катетов через пробел\n").split())
            return leg_1, leg_2
        except ValueError:
            print("Неправильно введены значения катетов. Пожалуйста, введите числовые значения.")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

leg_1, leg_2 = get_legs()
client.sendall(f"{leg_1}, {leg_2}".encode())

print(f'Гипотенуза = {client.recv(BUFFER_SIZE).decode()}')

