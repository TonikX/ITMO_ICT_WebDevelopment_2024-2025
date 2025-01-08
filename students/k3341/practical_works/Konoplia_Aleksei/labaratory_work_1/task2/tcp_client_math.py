import socket
import threading
import math

def tcp_client_math():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("localhost", 23456))
    print("Выберите операцию: 1 - Теорема Пифагора, 2 - Квадратное уравнение")
    operation = input("Введите номер операции: ")
    client_socket.sendall(operation.encode())

    if operation == "1":
        a = input("Введите сторону a: ")
        b = input("Введите сторону b: ")
        client_socket.sendall(a.encode())
        client_socket.sendall(b.encode())
    elif operation == "2":
        a = input("Введите коэффициент a: ")
        b = input("Введите коэффициент b: ")
        c = input("Введите коэффициент c: ")
        client_socket.sendall(a.encode())
        client_socket.sendall(b.encode())
        client_socket.sendall(c.encode())

    result = client_socket.recv(1024).decode()
    print(f"Результат: {result}")
    client_socket.close()
if __name__ == '__main__':
    tcp_client_math()