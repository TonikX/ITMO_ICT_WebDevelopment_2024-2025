import socket
import threading

# 定义全局变量
clients = []

# 处理客户端连接的函数
def handle_client(client_socket, client_address):
    print(f"[INFO] Клиент подключен: {client_address}")
    clients.append((client_socket, client_address))
    
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            if message:
                print(f"[Cообщение от {client_address}]: {message}")
                broadcast(message, client_address)
        except:
            print(f"[Отключение клиента]: {client_address}")
            clients.remove((client_socket, client_address))
            client_socket.close()
            break

# 广播消息的函数
def broadcast(message, sender_address):
    for client_socket, client_address in clients:
        if client_address != sender_address:  # 不发送给消息的发送者
            try:
                client_socket.send(f"\n[{sender_address[1]}]: {message}".encode("utf-8"))
            except:
                client_socket.close()
                clients.remove((client_socket, client_address))

# 主函数
def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 12345))  # 监听端口
    server.listen(5)
    print("[SERVER STARTED]")
    
    while True:
        client_socket, client_address = server.accept()
        threading.Thread(target=handle_client, args=(client_socket, client_address)).start()

if __name__ == "__main__":
    main()
