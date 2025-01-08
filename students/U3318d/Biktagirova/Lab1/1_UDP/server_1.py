import socket

serv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

HOST = 'localhost'
PORT = 8888
SERVER_MESSAGE = "Hello, client"
BUFF_SIZE = 1024
SERVER_MESSAGE_IN_BYTES = SERVER_MESSAGE.encode()

serv_socket.bind((HOST, PORT))
print("UDP server is running on", HOST, ':', PORT)

while True:
    try:
        # получаем данные размера BUFF_SIZE
        CLIENT_MESSAGE, address = serv_socket.recvfrom(BUFF_SIZE)
        # отправляем сообщение клиенту
        serv_socket.sendto(SERVER_MESSAGE_IN_BYTES, address)

        # выводим полученное сообщение от клиента декодированное из байтовой строки в строку
        print(CLIENT_MESSAGE.decode())

    except KeyboardInterrupt:
        print(f"Closing server on {HOST}:{PORT}")
        serv_socket.close()
        break
