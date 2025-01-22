import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                print(message)
            else:
                break
        except:
            break

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 4040))

# Запуск потока для получения сообщений
threading.Thread(target=receive_messages, args=(client_socket,)).start()

while True:
    message = input()
    if message:
        client_socket.send(message.encode())
