import socket

server_address = ('localhost', 14900)

def send_mark(name, value):
    http_method = 'POST'
    http_url = f"isu.ifmo.ru/pls/apex/f?name={name}&value={value}"
    http_version = "HTTP/1.1"
    data = f"{http_method} {http_url} {http_version}\nHost: example.local\n"

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(server_address)
    client.send(bytes(data, 'UTF-8'))

    data = client.recv(16384)
    print(data.decode("UTF-8"))

    client.close()

def get_marks(name):
    http_method = 'GET'
    http_url = f"isu.ifmo.ru/pls/apex/f?name={name}"
    http_version = "HTTP/1.1"
    data = f"{http_method} {http_url} {http_version}\nHost: example.local\n"

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(server_address)
    client.send(bytes(data, 'UTF-8'))

    data = client.recv(16384)
    print(data.decode("UTF-8"))

    client.close()

send_mark('ООП', 5)
get_marks('ООП')
get_marks('Математика')