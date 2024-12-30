import socket


a = float(input("Введите основание (a): "))
b = float(input("Введите сторону (b): "))
c = float(input("Введите высоту (h) или угол (alpha): "))

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("localhost", 7070))


client_socket.send(f"{a} {b} {c}".encode())


data = client_socket.recv(1024).decode()
print(f"Result from server: {data}")

client_socket.close()
