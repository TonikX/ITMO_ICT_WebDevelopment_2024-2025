import socket

con_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
con_client.connect(('localhost', 8090))
msg = input('Напишите длину одной из сторон и длину высоты,опущенной на эту сторону. Через пробел')
con_client.send(msg.encode())
result = con_client.recv(1024).decode()
print(f"Площадь параллелограмма: {result}")
con_client.close()
