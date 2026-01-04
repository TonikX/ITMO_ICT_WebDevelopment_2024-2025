import socket

HOST = "localhost"
PORT = 8080

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    print("Решение квадратного уравнения ax^2 + bx + c = 0")
    a = input("Введите a: ")
    b = input("Введите b: ")
    c = input("Введите c: ")

    client_socket.send(f"{a} {b} {c}".encode("utf-8"))

    result = client_socket.recv(1024).decode("utf-8")
    print("Результат от сервера:", result)

    client_socket.close()

if __name__ == "__main__":
    main()
