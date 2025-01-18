import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('127.0.0.1', 65432))
while True:
    a = input("Введите катет a: ")
    b = input("Введите катет b: ")
    if a == "exit" or b == "exit":
        break
    sock.sendall(f"{a} {b}".encode('utf-8'))
    data = sock.recv(1024).decode('utf-8')
    print(f"Гипотенуза: {data}")