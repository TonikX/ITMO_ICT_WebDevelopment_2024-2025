import socket

def udp_server(host='127.0.0.2', port=12345):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))
    print(f"Сервер запущен")
    while True:
        data, addr = sock.recvfrom(1024)
        print(f"Получено сообщение: {data.decode()}")
        response = 'Hello, client'
        sock.sendto(response.encode(), addr)

if __name__ == "__main__":
    udp_server()
