import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('localhost', 8080))

data, client_address = server_socket.recvfrom(1024)
print(f"Получено сообщение от клиента: {data.decode()}")

response = "Hello, client"
server_socket.sendto(response.encode(), client_address)

server_socket.close()