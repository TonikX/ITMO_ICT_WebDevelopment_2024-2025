import socket

port = 12345
buffer_size = 1024

def math_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', port))

    a = input("Введите длину катета a: ")
    b = input("Введите длину катета b: ")

    client_socket.sendall(f"{a},{b}".encode('utf-8'))

    result = client_socket.recv(buffer_size).decode('utf-8')
    print(f"Гипотенуза: {result}")

    client_socket.close()

if __name__ == "__main__":
    math_client()