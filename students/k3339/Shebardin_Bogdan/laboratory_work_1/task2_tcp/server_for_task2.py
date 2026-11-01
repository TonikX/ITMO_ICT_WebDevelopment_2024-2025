import socket

new_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
new_socket.bind(('localhost',8080))
new_socket.listen(5)
print("server was started")
conn, addr = new_socket.accept()
print("connected:", addr)


message = "выберете дейстриве: 1. площадь трапеции"
message2 = "напишите верхнее, нижнее основания и высоту через пробел"

while True:
    conn.send(message.encode("utf-8"))
    data = conn.recv(1024)
    data = data.decode("utf-8")
    if data != "1" or not data:
        break
    conn.send(message2.encode("utf-8"))
    answer = conn.recv(1024)
    answer = answer.decode("utf-8")
    x = int(answer.split(" ")[0])
    y = int(answer.split(" ")[1])
    z = int(answer.split(" ")[2])
    result = ((x+y)/2)*z
    print(result)
    conn.send(str(result).encode("utf-8") + b'\n')

conn.close()




