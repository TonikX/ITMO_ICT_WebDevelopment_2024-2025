import socket
from threading import Thread

HOST = 'localhost'
PORT = 8080

client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_sock.connect((HOST, PORT))


def receive():
    while True:
        try:
            message = client_sock.recv(1024).decode()
            if message:
                print(message)
            else:
                print("Сервер закрыл соединение")
                break
        except Exception as e:
            print(f"Ошибка при получении сообщения: {e}")
            break

def send():
    while True:
        message = input()
        client_sock.send(message.encode())
        if message.lower() == "exit":
            print("Выход из чата")
            client_sock.close()
            break


receive_thread = Thread(target=receive)
receive_thread.start()

send_thread = Thread(target=send)
send_thread.start()

receive_thread.join()
send_thread.join()
