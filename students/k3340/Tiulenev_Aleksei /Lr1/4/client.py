import socket
import threading

HOST = "127.0.0.1"
PORT = 1234
BUFFER_SIZE = 1024

USERNAME = input("Введите ваше имя: ")

def receive_messages(connection):
    while True:
        try:
            data = connection.recv(BUFFER_SIZE).decode('utf-8')
            if data:
                print(data)
            else:
                # Соединение закрыто
                print("Соединение с сервером потеряно.")
                break
        except:
            print("Произошла ошибка при получении данных.")
            break

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
client_socket.send((USERNAME + '\n').encode('utf-8'))

threading.Thread(target=receive_messages, args=(client_socket,)).start()

print("Вы можете начинать отправлять сообщения. Для выхода введите 'quit'.")

while True:
    message = input()
    if message.lower() == 'quit':
        client_socket.send('quit\n'.encode('utf-8'))
        client_socket.close()
        break
    else:
        client_socket.send((message + '\n').encode('utf-8'))
