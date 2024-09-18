import socket

def main():
    conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    conn.bind(("localhost", 12345))

    data, address = conn.recvfrom(1024)
    print(data.decode())

    conn.sendto("Hello, client".encode(), address)
    conn.close()


if __name__ == "__main__":
    main()
