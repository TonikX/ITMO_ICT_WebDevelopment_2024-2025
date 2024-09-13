import socket


buffer_size = 1024
port = 8080
host = 'localhost'
server_address = (host, port)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

client_socket.sendto(b"Hello server", server_address)
response, server = client_socket.recvfrom(buffer_size)
print(f"Ответ от сервера: {response.decode()}")

client_socket.close()
