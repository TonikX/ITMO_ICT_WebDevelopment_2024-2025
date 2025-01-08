import socket
import threading


def receive(client):
    while True:
        try:
            message = client.recv(BUFF_SIZE).decode()
            if message:
                print(message)
            else:
                print("Server has closed the connection.")
                break
        except Exception as e:
            print(f"Error receiving message: {e}")
            break
    client.close()
    exit()


def write(client, nickname):
    while True:
        try:
            message = f'{nickname}: {input("")}'
            client.send(message.encode())
        except:
            print(f"Error sending message")
            break


if __name__ == '__main__':
    PORT = 8080
    HOST = 'localhost'
    BUFF_SIZE = 1024

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((HOST, PORT))
    except:
        print(f"Error connecting to server")
        exit()

    nick = input("Welcome to the chat! What's your nickname? ")

    client_socket.send(nick.encode())

    receive_th = threading.Thread(target=receive, args=(client_socket,))
    receive_th.start()

    write_th = threading.Thread(target=write, args=(client_socket, nick))
    write_th.start()

    receive_th.join()
    write_th.join()
