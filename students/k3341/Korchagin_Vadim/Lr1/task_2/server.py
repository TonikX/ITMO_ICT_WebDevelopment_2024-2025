import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 1236))
s.listen(5)
message_recevied = []
message_count = 0


def pif(a, b):
    return float((a ** 2 + b ** 2) ** 0.5)


clientsocket, address = s.accept()

while True:
    try:
        data = clientsocket.recv(1024)
        if data:
            udata = data.decode('utf-8')
            message_count += 1
            message_recevied.append(udata)
            if message_count % 2 == 0:
                clientsocket.send(f"{pif(int(message_recevied[-1]), int(message_recevied[-2]))}".encode('utf-8'))
    except KeyboardInterrupt:
        s.close()
