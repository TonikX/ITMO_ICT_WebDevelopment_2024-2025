import socket

if __name__ == "__main__":
    ip = socket.gethostbyname('localhost')
    print(ip)