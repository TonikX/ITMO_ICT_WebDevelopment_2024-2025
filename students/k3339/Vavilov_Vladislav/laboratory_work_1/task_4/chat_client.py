import socket
import threading

HOST = "127.0.0.1"
PORT = 12347

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

name = input("Введите имя: ")
client.sendall((name + "\n").encode())


def receive_messages():
    while True:
        try:
            data = client.recv(1024)

            if not data:
                break

            print(data.decode(), end="", flush=True)

        except OSError:
            break


threading.Thread(target=receive_messages, daemon=True).start()

try:
    while True:
        message = input()

        client.sendall((message + "\n").encode())

        if message == "/exit":
            break

except (KeyboardInterrupt, EOFError, OSError, UnicodeError):
    pass

finally:
    client.close()