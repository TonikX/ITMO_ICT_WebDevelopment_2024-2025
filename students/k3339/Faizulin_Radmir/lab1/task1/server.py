import socket

serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ("127.0.0.1", 7777)
serverSock.bind(server_address)
print("Сервер запущен ;)")

try:
    while True:
        data, client_address = serverSock.recvfrom(1024)
        print(f"Сообщение от клиента {client_address}: {data.decode()}")

        response = "Hello, client"
        serverSock.sendto(response.encode(), client_address)
        print(f"Ответ отправлен клиенту {client_address}")
except Exception as serverExc:
    print(f"Ошибка: {serverExc}")
finally:
    serverSock.close()
    print("Сервер остановлен.")
