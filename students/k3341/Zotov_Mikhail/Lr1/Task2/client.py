import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 2024)
sock.connect(server_address)

while True:
    message = input('Enter the coefficients of the equation (Enter to exit): ')
    if not message:
        break

    sock.send(message.encode())

    result = sock.recv(1024)
    print(result.decode())

sock.close()
