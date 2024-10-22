import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((socket.gethostname(), 1234))

while True:
    try:
        data, addr = s.recvfrom(1024)
        udata = data.decode("utf-8")
        print(f"Connection established: {addr}")
        print("Received message: %s" % udata)
        MESSAGE = b'Hello, client!'
        s.sendto(MESSAGE, addr)
    except KeyboardInterrupt:
        s.close()
        break
