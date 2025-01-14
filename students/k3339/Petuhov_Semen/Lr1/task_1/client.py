import socket

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', 1936)

message = "Hello, server"
#Отправка сообщения при запуске
client.sendto(message.encode(), server_address)
#Получение сообщения
data, sender_addr = client.recvfrom(1024)
print("Message from server:", data.decode())
client.close()