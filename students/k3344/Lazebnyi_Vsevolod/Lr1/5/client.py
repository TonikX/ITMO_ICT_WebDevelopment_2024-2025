import socket

def send_get_request(host, port):
    request = "GET / HTTP/1.1\r\nHost: {}\r\n\r\n".format(host)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        client_socket.sendall(request.encode('utf-8'))
        response = client_socket.recv(4096).decode('utf-8')
        print("GET response: \n", response)

def send_post_request(host, port, discipline, grade):
    body = "discipline={}&grade={}".format(discipline, grade)
    request = "POST / HTTP/1.1\r\nHost: {}\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: {}\r\n\r\n{}".format(host, len(body), body)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        client_socket.sendall(request.encode('utf-8'))
        response = client_socket.recv(4096).decode('utf-8')
        print("POST response: \n", response)

if __name__ == '__main__':
    host = "localhost"
    port = 8080

    # Отправка POST запроса для добавления новой оценки
    send_post_request(host, port, "Math", "4")
    send_post_request(host, port, "WEB", "5")
    send_post_request(host, port, "FRONT", "5")
    send_post_request(host, port, "DATABASE", "5")

    # Отправка GET запроса для получения списка всех оценок
    send_get_request(host, port)
