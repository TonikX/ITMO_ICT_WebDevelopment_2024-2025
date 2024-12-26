import socket

server_address = ('localhost', 14900)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    coefficients = list(map(int, input("Введите коэффициенты a, b, c: ").split()))
except Exception:
    coefficients = None
    print('Ошибка! Неправильный формат коэффициентов!')

if coefficients is not None:
    coefficients = bytes(' '.join([str(coefficient) for coefficient in coefficients]), 'UTF-8')

    client.connect(server_address)
    client.send(coefficients)

    data = client.recv(16384)
    print(data.decode("UTF-8"))

    client.close()


