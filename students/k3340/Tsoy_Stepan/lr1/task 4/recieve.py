import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(message)
        except:
            client_socket.close()
            break

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12366))

threading.Thread(target=receive_messages, args=(client_socket,)).start()

print("Подключение к серверу установлено. Введите сообщение:")
while True:
    message = input()
    client_socket.send(message.encode('utf-8'))
