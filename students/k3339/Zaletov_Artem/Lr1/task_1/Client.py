import socket

def udp_client(host='127.0.0.2', port=12345):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    message = 'Hello, server'
    sock.sendto(message.encode(), (host, port))
    data, addr = sock.recvfrom(1024)  # Буфер 1024 байта
    print(f"Получено сообщение : {data.decode()}")

if __name__ == "__main__":
    udp_client()

