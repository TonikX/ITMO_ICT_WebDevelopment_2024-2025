import socket
import threading


def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode()
            if message:
                print(message)
        except:
            print("Соединение потеряно")
            sock.close()
            break

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))

threading.Thread(target=receive_messages, args=(client_socket,)).start()

name = input("Введите ваше имя: ")
client_socket.send(name.encode())

while True:
    message = input()
    client_socket.send(message.encode())