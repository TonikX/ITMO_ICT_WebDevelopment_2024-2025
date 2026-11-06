import socket

a = float(input("Введите основание параллелограмма: "))
h = float(input("Введите высоту параллелограмма: "))

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 12346))

client.sendall(f"{a} {h}".encode())

result = client.recv(1024).decode()
print("Площадь параллелограмма:", result)

client.close()