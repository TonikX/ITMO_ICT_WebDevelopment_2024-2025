import socket
import threading

clients = {}

def broadcast(message, sender_conn):
    for client_conn, user_name in clients.items():
        if client_conn != sender_conn:
            try:
                client_conn.send(message)
            except:
                client_conn.close()
                del clients[client_conn]


def client_chat(conn, cl_id):
    user_name = conn.recv(1024).decode()
    clients[conn] = user_name
    print(f"Клиент {user_name} подключен с адресом {cl_id}")

    try:
        while True:

            data = conn.recv(1024)
            if not data:
                break

            message = f"{clients[conn]}: {data.decode('utf-8')}".encode('utf-8')
            print(f"Сообщение от {clients[conn]}: {data.decode('utf-8')}")

            broadcast(message, conn)
    except ConnectionError:
        print(f"Клиент {clients[conn]} отключился")
    finally:
        conn.close()
        del clients[conn]
        print(f"Соединение с {cl_id} закрыто")


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
PORT = 8000
server_socket.bind(("127.0.0.1", PORT))
server_socket.listen(5)

print(f"Сервер запущен на 127.0.0.1:{PORT}")

while True:
    conn, cl_id = server_socket.accept()
    print(f"Подключен новый клиент: {cl_id}")


    client_thread = threading.Thread(target=client_chat, args=(conn, cl_id))
    client_thread.start()
