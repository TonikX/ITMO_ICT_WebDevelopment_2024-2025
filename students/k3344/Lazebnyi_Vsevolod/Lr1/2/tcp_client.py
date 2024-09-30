import socket

a, b, c = input("Введите коэффициент a: "), (input("Введите коэффициент b: ")), (input("Введите коэффициент c: "))
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("localhost", 8080))
try:
    client_socket.send(f"{a}, {b}, {c}".encode())
    server_message = client_socket.recv(1024).decode()
    print(f"Результат: {server_message}")
finally:
    client_socket.close()