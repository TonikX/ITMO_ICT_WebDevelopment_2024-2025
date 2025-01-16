import socket
import threading

# 处理接收消息的函数
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            if message:
                print(message)
        except:
            print("[Соединение закрыто]")
            client_socket.close()
            break

# 主函数
def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 12345))  # 连接到服务器

    threading.Thread(target=receive_messages, args=(client,)).start()
    
    while True:
        message = input("Вы: ")
        if message.lower() == "exit":
            client.close()
            break
        client.send(message.encode("utf-8"))

if __name__ == "__main__":
    main()
