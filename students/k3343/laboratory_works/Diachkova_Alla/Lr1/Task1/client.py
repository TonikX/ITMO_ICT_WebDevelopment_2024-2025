import socket


def connect():
    serverIP = "127.0.0.1"
    portNumber = 8080
    bufferSize = 1024

    msgFromClient = "Hello, server!"

    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    UDPClientSocket.sendto(str.encode(msgFromClient), (serverIP, portNumber))
    msgFromServer = UDPClientSocket.recvfrom(bufferSize)
    msg = "Message from Server: {}".format(msgFromServer[0].decode())

    print(msg)


if __name__ == "__main__":
    connect()
