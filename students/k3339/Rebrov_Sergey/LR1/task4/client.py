import socket
import threading

name = input("Введите имя: ")


def receive_messages(client_sock):
    while True:
        try:
            print(client_sock.recv(1024).decode())
        except:
            print("** Ошибка подключения. **")
            client_sock.close()
            break


def send_messages(client_sock):
    while True:
        try:
            client_sock.send(input().encode('utf-8'))
        except:
            print("** Ошибка отправки сообщения. **")
            client_sock.close()
            break


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 8080))

client_socket.send(name.encode())

receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
receive_thread.start()

send_thread = threading.Thread(target=send_messages, args=(client_socket,))
send_thread.start()

print("** Вы присоединились к чату! **")
