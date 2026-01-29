import socket
import threading

nickname = input("Введите свой никнейм: ")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("localhost", 8080))


def recieve():
    while True:
        try:
            msg = client_socket.recv(1024).decode()
            if msg == "NICKNAME":
                client_socket.send(nickname.encode())
            else:
                print(msg)
        except:
            print('[ОШИБКА] Соединение с сервером потеряно')
            client_socket.close()
            break


def write():
    while True:
        msg = f"[{nickname}]: {input()}"
        client_socket.send(msg.encode())


recieve_thread = threading.Thread(target=recieve)
recieve_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()

