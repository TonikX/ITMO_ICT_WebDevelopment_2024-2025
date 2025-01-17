import socket


def start_client(host, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((host, port))

        a = input("Введите длину первого катета: ")
        b = input("Введите длину второго катета: ")

        client.sendall(f"{a} {b}".encode())

        result = client.recv(1024).decode()
        print(f"Ответ от сервера: {result}")

    finally:
        client.close()


if __name__ == "__main__":
    start_client('127.0.0.1', 65432)
