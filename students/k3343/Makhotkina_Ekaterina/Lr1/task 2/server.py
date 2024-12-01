import socket

def area_parallelogram(a, h):
    return a * h

def check(x):
    if x <= 0:
        return False
    else: return True

def connection():
        host = '127.0.0.1'
        port = 5555

        server_socket = socket.socket()
        server_socket.bind((host, port))

        server_socket.listen()
        conn, addr = server_socket.accept()

        print('Соединение установлено с', addr)

        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            a, h = map(int, data.split())
            result = area_parallelogram(a, h)
            conn.send(str(result).encode())
            print(f'Отправлен результат: {result}')

        conn.close()

if __name__ == "__main__":
    connection()
