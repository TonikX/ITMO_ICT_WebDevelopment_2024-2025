import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_socket.bind(('localhost', 8080))

print("Сервер запущен")

while True:
    request, client_address = server_socket.recvfrom(1024)
    print(f'Запрос от {client_address}: {request.decode()}')
    response = 'Hello, Client!'
    server_socket.sendto(response.encode(), client_address)
    # request.close()
