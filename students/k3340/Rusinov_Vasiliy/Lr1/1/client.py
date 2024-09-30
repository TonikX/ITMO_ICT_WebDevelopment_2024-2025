import socket
client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)# socket.AF_INET — используется для указания семейства адресов IPv4.
#socket.SOCK_DGRAM — указывает, что будем использовать протокол UDP (для TCP используется SOCK_STREAM)
server_address = ('localhost',14900)
message = "Hello, server"
client_sock.sendto(message.encode(),server_address)
data, server_address = client_sock.recvfrom(1024)
print(f"Сообщение от сервера: {data.decode()}")
client_sock.close()
