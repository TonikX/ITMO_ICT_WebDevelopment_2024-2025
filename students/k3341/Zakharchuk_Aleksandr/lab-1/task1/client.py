import socket


def main():
    conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    conn.connect(("localhost", 12345))

    conn.send("Hello, server".encode())

    data = conn.recv(1024)
    print(data.decode())


if __name__ == "__main__":
    main()
