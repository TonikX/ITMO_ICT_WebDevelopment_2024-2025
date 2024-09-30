import socket

con_sever = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
con_sever.bind(('localhost', 8090))
con_sever.listen(1)

while True:
    clin_socket, clin_addr = con_sever.accept()
    data = clin_socket.recv(1024)
    print(data.decode())
    a, h = str(data.decode()).split(' ')
    result = int(a) * int(h)
    clin_socket.send(str(result).encode())

con_sever.close()
