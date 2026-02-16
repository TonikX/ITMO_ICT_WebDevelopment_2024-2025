import socket
import threading

def receive(sock):
    while True:
        try:
            msg = sock.recv(1024).decode("utf-8", errors="ignore")
            if msg:
                print(msg)
            else:
                break
        except:
            break

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("127.0.0.1", 12345))

nickname = input("Введите свой ник: ") # спрашиваем имя
sock.send(nickname.encode("utf-8", errors="ignore"))

thread = threading.Thread(target=receive, args=(sock,)) # запускаем поток для приёма сообщений
thread.start()

print("Теперь можно писать сообщения")
while True:
    msg = input()
    sock.send(msg.encode("utf-8", errors="ignore"))
