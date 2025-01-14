import socket

#Создание сокета для связи по UDP
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', 1936)
#Привязка сокета к адресу
server.bind(server_address)
#Обработчик сообщений
while True:
    #Ожидание сообщения
    data, client_address = server.recvfrom(1024)
    print("Message from client:", data.decode())
    response = "Hello, client"
    #Ответ
    server.sendto(response.encode(), client_address)