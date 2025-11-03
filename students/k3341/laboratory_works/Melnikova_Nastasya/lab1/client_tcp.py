import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # создаём TCP сокет

sock.connect(("127.0.0.1", 12345)) # подключаемся к серверу

a = input("Введите a: ")
b = input("Введите b: ")

sock.send((a + " " + b).encode()) # отправляем строку "a b"

result = sock.recv(1024).decode() # ждём результат
print("Результат:", result)

sock.close()