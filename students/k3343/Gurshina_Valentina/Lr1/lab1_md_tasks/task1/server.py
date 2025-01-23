import socket

udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #последний отвечает за протокол UDP
udp_server.bind(("127.0.0.1", 9090))  # порт 9090
udp_server.settimeout(1)  # тайм-аут до 1

try:
    while True:
        try:
            message, client_address = udp_server.recvfrom(1024)
            print(f"Received message: {message.decode()}")
            udp_server.sendto("Hello, client".encode(), client_address)
        except socket.timeout:
            pass  # пропускаем время ожидания

except KeyboardInterrupt:
    udp_server.close()
    print("Server closed.")
