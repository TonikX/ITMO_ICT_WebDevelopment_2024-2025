import socket


conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.bind(('127.0.0.1', 14900))
conn.listen(10)

while True:
    try:
        clientsocket, address = conn.accept()
        data = clientsocket.recv(16384)
        udata = data.decode("utf-8").split()
        S = int(udata[0]) * int(udata[1])
        print(f'Основание a: {udata[0]}, выcота h: {udata[1]}')
        print(f'Площадь параллелогграмма: {S}')
    except KeyboardInterrupt:
        conn.close()
        break