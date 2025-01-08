import socket

# UDP
client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

HOST = 'localhost'
PORT = 8888
CLIENT_MESSAGE = "Hello, server"
CLIENT_MESSAGE_IN_BYTES = CLIENT_MESSAGE.encode()
BUFF_SIZE = 1024

# подключаемся
client_sock.connect((HOST, PORT))

# отправляем сообщение
client_sock.send(CLIENT_MESSAGE_IN_BYTES)

# а это можно использовать без отдельного connect
# client_sock.sendto(CLIENT_MESSAGE_IN_BYTES, (HOST, PORT))

try:
    SERVER_MESSAGE = client_sock.recv(BUFF_SIZE).decode()
except ConnectionRefusedError:
    SERVER_MESSAGE = f'Sorry, connection to {HOST}:{PORT} is refused'

print(SERVER_MESSAGE)

