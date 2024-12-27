import socket

HOST = 'localhost'
PORT = 8091
BUF_SIZE = 1024


def calculate_trapez_area(a, b, h):
    return ((a + b) * h) / 2


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # stream тк TCP
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(f"Server online on {HOST}:{PORT}")

    while True:
        connection, address = server_socket.accept()
        print(f"Connection with {address}")

        client_data = connection.recv(BUF_SIZE).decode()
        if not client_data:
            break
        try:
            a, b, h = map(float, client_data.split(','))
            data = f"Got data: a = {a} , b = {b} , h = {h}"
            print(data)
            area = calculate_trapez_area(a, b, h)
            answer = f"Area of trapez: {area:.2f}"
        except ValueError:
            answer = "Error: send int"
        print(f"Answer has been sent, answer: {area}")
        connection.sendall(answer.encode())
        connection.close()
    server_socket.close()


if __name__ == "__main__":
    main()
