import socket

HOST = 'localhost'
PORT = 9090

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT))
    print("UDP server is running...")

    while True:
        data, addr = sock.recvfrom(1024)
        print(f"Received from {addr}: {data.decode()}")
        sock.sendto("Hello client!".encode(), addr)


if __name__ == "__main__":
    main()