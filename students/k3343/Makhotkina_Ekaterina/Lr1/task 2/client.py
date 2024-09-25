import socket

def connection():
    host = '127.0.0.1'
    port = 5555

    client_socket = socket.socket()
    client_socket.connect((host, port))

    a = int(input("Введите длину стороны a: "))
    h = int(input("Введите высоту h: "))

    message = f"{a} {h}"
    client_socket.send(message.encode())

    result = client_socket.recv(1024).decode()
    print(f"Площадь параллелограмма: {result}")

    client_socket.close()

if __name__ == "__main__":
    connection()
