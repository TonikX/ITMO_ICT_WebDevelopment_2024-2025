import socket

con_sever = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
con_sever.bind(('localhost', 9090))

while True:
    data,adr = con_sever.recvfrom(1024)
    print(data.decode())
    con_sever.sendto(b'Hello, client',adr)
    if not data:
        break

con_sever.close()