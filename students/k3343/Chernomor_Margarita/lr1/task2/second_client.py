import socket


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12346))


base = float(input("Введите основание параллелограмма: "))
height = float(input("Введите высоту параллелограмма: "))


client_socket.send(f"{base} {height}".encode('utf-8'))


result = client_socket.recv(1024).decode('utf-8')
print(f"Площадь параллелограмма: {result}")

client_socket.close()
