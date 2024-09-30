import socket
from threading import Thread


# функция нужна для старта приёма сообщений
def accept_incoming_connections():
    while True:
        client, client_address = sock.accept()
        # выведите информацию о подключении
        print(f'Сonnected: {client_address}')
        # попросите ввести имя
        client.send(b'Write your name')
        # добавьте адрес клиента в словарь addresses
        addresses[client] = client_address

        Thread(target=handle_client, args=(client, client_address)).start()


# функция обрабатывает сообщения одного клиента
def handle_client(client, addres):
    # получите сообщение с именем клиента и поприветсвуйте его
    name = client.recv(1024).decode()
    clients[client] = name
    # используя функцию broadcast() напишите всем участникам чата, что к нему присоединился текущий клиент
    msg_welcome = f'Welcome {name}!'
    client.send(msg_welcome.encode())
    msg_welcome1 = f'Server:Say hi to {name}'
    broadcast(bytes(msg_welcome1, "utf-8"))
    # добавьте имя клиента в словарь clients (в качестве ключей - сокеты клиентов)

    # получайте сообщения от клиентов в чате
    while True:
        try:
            msg = client.recv(1024)
            print(name, msg.decode())
            broadcast(msg, name)
        except:
            continue


# функция отправляет сообщения всем клиентам
def broadcast(message, name=""):
    for sock in clients:
        sock.send(name.encode() + b' ' + message)


def server_message():
    while True:
        out_data = input('').encode()
        broadcast(out_data, name='Server')


clients = {}
addresses = {}
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('localhost', 6090))
sock.listen()
print("Waiting for connection...")
out_thread = Thread(target=server_message)
out_thread.start()
accept_thread = Thread(target=accept_incoming_connections)
accept_thread.start()
accept_thread.join()
sock.close()
