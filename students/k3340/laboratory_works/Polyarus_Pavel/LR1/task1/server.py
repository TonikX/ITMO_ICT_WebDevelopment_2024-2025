import socket 


with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind(('localhost', 8080))
    print("UDP сервер запущен на порту 8080")

    while True:
        data, addr = s.recvfrom(1024)
        if not data:
            continue
        
        print(f'Подключение от {addr}\n Запрос: {data.decode()}')

        msg = "Hello, client!"
        s.sendto(msg.encode(), addr)
