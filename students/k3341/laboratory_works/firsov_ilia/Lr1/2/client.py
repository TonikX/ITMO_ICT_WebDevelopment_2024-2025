import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 65432)
client_socket.connect(server_address)

try:
    print("Enter trapezoid parameters:")
    a = float(input("Enter the first base (a): "))
    b = float(input("Enter the second base (b): "))
    h = float(input("Enter the height (h): "))

    message = f"{a}, {b}, {h}"
    client_socket.sendall(message.encode())

    result = client_socket.recv(1024).decode()
    print(f"Trapezoid area: {result}")
finally:
    client_socket.close()