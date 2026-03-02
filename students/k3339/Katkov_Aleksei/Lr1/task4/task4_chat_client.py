import socket
import threading

HOST = "127.0.0.1"
PORT = 14000
BUFFER_SIZE = 1024


def receive_loop(sock: socket.socket):
    while True:
        try:
            data = sock.recv(BUFFER_SIZE)
        except OSError:
            break

        if not data:
            break

        print(data.decode("utf-8"), end="")

    print("Соединение с сервером закрыто.")


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    print("Подключено к чату. Пиши сообщения, для выхода — exit")

    thread = threading.Thread(target=receive_loop, args=(sock,), daemon=True)
    thread.start()

    while True:
        msg = input()
        if msg.lower() == "exit":
            break
        sock.sendall((msg + "\n").encode("utf-8"))

    sock.close()


if __name__ == "__main__":
    main()
