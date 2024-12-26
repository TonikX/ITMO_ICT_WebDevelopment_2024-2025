import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv_address = ('localhost', 8080)
sock.connect(serv_address)

try:
    a = input('length of side a: ')
    b = input('length of side b: ')
    sock.sendall(f'{a} {b}'.encode())

    data = sock.recv(1024).decode()
    print(data)

finally:
    sock.close()
