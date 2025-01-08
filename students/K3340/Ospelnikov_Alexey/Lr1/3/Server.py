import socket


socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind(('', 8080))

max_conn_count = 5

socket.listen(max_conn_count)

while True:
    conn_socket, addr = socket.accept()
    request = conn_socket.recv(1024).decode().split()
    if request[0] != "GET":
        conn_socket.close()
        print("Bad Gateway")
        conn_socket.send(b'Response 400')
        conn_socket.close()
        break
    print(request)
    with open('index.html', 'r') as index:
        response = 'Response 200'
        print("OK")
        conn_socket.send(response.encode('utf-8'))
        conn_socket.close()