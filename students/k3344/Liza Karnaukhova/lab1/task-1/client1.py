import socket
con_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
con_client.connect(('localhost', 9090))
con_client.sendto(b'Hello, server', ('localhost', 9090))

while True:
    data,adr = con_client.recvfrom(1024)
    print(data.decode())

con_client.close()
