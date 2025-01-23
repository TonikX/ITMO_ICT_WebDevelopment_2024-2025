import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("127.0.0.1", 9090))
server_socket.listen(10)
server_socket.settimeout(1)

try:
    while True:
        try:
            client_socket, address = server_socket.accept()
            client_socket.send(
                "Введите через запятую без пробелов значения a, b и h".encode()
            )

            data = client_socket.recv(1024).decode()
            try:
                a, b, h = (float(num) for num in data.split(","))
                calculation = (a + b) / 2 * h
                client_socket.send(f"Площадь трапеции: {calculation}".encode())
            except ValueError:
                client_socket.send("Ошибка ввода: убедитесь, что введены числа через запятую.".encode())

            client_socket.close()  # закрываем соединение с клиентом

        except socket.timeout:
            pass

except KeyboardInterrupt:
    server_socket.close()
