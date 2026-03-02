import socket

HOST = 'localhost'
PORT = 9090

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto("Hello, server!".encode(), (HOST, PORT))
    data, addr = sock.recvfrom(1024)
    print("Server:", data.decode())
    sock.close()

if __name__ == '__main__':
    main()