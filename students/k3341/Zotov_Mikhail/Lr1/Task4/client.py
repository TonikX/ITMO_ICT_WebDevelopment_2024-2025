import socket
import threading


def run():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 2024)
    sock.connect(server_address)
    message = sock.recv(1024)
    print(message.decode())
    nickname = input('Nickname: ')
    sock.send(nickname.encode())

    threading.Thread(target=accept_messages, args=(sock,)).start()
    threading.Thread(target=send_messages, args=(sock,)).start()


def send_messages(sock):
    while True:
        message = input("")
        sock.sendall(message.encode())


def accept_messages(sock):
    while True:
        message = sock.recv(1024)
        print(message.decode())


if __name__ == '__main__':
    run()
