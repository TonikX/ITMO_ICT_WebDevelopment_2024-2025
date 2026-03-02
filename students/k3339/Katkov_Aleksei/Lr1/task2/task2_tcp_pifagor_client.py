import socket

HOST = "127.0.0.1"
PORT = 13000
BUFFER_SIZE = 1024

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((HOST, PORT))
        print("Подключено к серверу Пифагора.")
        print("Введите катеты a и b через пробел. Для выхода введите 'exit'.")

        while True:
            user_input = input("a b > ")

            if user_input.strip().lower() == "exit":
                print("Отключение от сервера.")
                break

            client.sendall((user_input + "\n").encode("utf-8"))

            response = client.recv(BUFFER_SIZE).decode("utf-8")
            print("Ответ сервера:", response.strip())

if __name__ == "__main__":
    main()
