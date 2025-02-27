import socket

HOST = 'localhost'
PORT = 5005

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    while True:
        conn, addr = s.accept()
        with conn:
            print('Подключен клиент:', addr)
            data = conn.recv(1024)
            if data:
                response = b'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n'
                with open('index.html', 'rb') as f:
                    response += f.read()
                conn.sendall(response)
