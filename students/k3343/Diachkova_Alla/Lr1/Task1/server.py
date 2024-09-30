import socket

def connect():
    localIP = "127.0.0.1"
    localPort = 8080
    bufferSize = 1024

    msgFromServer = "Hello, client!"
    bytesToSend = str.encode(msgFromServer)

    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    UDPServerSocket.bind((localIP, localPort))
    print("UDP server up and listening")

    while True:
        message, address = UDPServerSocket.recvfrom(bufferSize)
        clientMsg = "Message from Client: {}".format(message.decode())

        print(clientMsg)

        UDPServerSocket.sendto(bytesToSend, address)


if __name__ == "__main__":
    connect()
