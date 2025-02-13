import socket

def send_post_request(discipline, grade, host='127.0.0.1', port=8080):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    post_data = f"discipline={discipline}&grade={grade}"
    request = f"POST / HTTP/1.1\r\nHost: {host}\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: {len(post_data)}\r\n\r\n{post_data}"
    
    client_socket.send(request.encode())

    response = client_socket.recv(1024).decode()
    print("Ответ от сервера:", response)

    client_socket.close()

def send_get_request(host='127.0.0.1', port=8080):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    request = "GET / HTTP/1.1\r\nHost: {host}\r\n\r\n"
    client_socket.send(request.encode())

    response = client_socket.recv(1024).decode()
    print("Ответ от сервера:", response)

    client_socket.close()

if __name__ == "__main__":
    send_post_request("maths", "f")
    send_post_request("literature", "13")
    send_get_request()
