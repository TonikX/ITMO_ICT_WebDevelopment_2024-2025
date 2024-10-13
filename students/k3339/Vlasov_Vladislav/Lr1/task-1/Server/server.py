import socket

sock = socket.socket()

sock.bind(("", 14901))

sock.listen(5)

isListen = True
while isListen:
    conn, _ = sock.accept()
    request = conn.recv(1024)
    print(f"Request: {request.decode("utf-8")}")
    conn.send(b"Hello, client")