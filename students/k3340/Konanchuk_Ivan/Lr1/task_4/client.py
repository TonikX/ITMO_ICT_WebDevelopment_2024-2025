import socket
import threading

HOST = "127.0.0.1"
PORT = 50003

COLORS = {
    "1": ("Красный", "\033[31m"),
    "2": ("Зелёный", "\033[32m"),
    "3": ("Жёлтый", "\033[33m"),
    "4": ("Синий", "\033[34m"),
    "5": ("Пурпурный", "\033[35m"),
    "6": ("Голубой", "\033[36m"),
    "7": ("Белый", "\033[37m"),
    "8": ("Оранжевый", "\033[38;5;208m"),
}
RESET = "\033[0m"


def choose_color():
    print("Выберите цвет имени:")
    for number, (title, color) in COLORS.items():
        print(f"{number}. {color}{title}{RESET}")

    while True:
        choice = input("Ваш выбор (1-8): ")
        if choice in COLORS:
            return choice
        print("Нет такого номера, попробуйте ещё раз")


def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024).decode()
        except OSError:
            break  # сокет закрыли из основного потока после /exit

        if not data:
            print("Соединение с сервером закрыто")
            break
        print(data)


name = input("Введите имя: ")
color_num = choose_color()

my_color = COLORS[color_num][1]

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
client.send(f"{name}|{color_num}".encode())

thread = threading.Thread(target=receive_messages, args=(client,), daemon=True)
thread.start()

print("Чат открыт. Для выхода введите /exit")
while True:
    text = input()
    client.send(text.encode())
    if text == "/exit":
        break
    print(f"{my_color}Вы{RESET}: {text}")

client.close()
