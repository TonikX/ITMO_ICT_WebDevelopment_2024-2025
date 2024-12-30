import socket
import random
from Crypto.Util.number import bytes_to_long
from datetime import datetime
from threading import Thread
from colorama import Fore, init
init()

colors = [Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.LIGHTBLACK_EX, 
    Fore.LIGHTBLUE_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX, 
    Fore.LIGHTMAGENTA_EX, Fore.LIGHTRED_EX, Fore.LIGHTWHITE_EX, 
    Fore.LIGHTYELLOW_EX, Fore.MAGENTA, Fore.RED, Fore.WHITE, Fore.YELLOW
]

HOST = '127.0.0.1'
PORT = 16000
name = input('Enter your name: ')
seed = bytes_to_long(name.encode())
r = random.Random(seed)
color = r.choice(colors)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

def listen_for_messages():
    while True:
        try:
            message = client.recv(1024).decode()
            print('\n' + message)
        except Exception:
            pass

t = Thread(target=listen_for_messages)
t.daemon = True
t.start()

while True:
    try:
        msg = input()
        if msg.lower() == 'q':
            break
        date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        to_send = f'{color}[{date_now}] {name}: {msg}{Fore.RESET}'
        client.sendall(to_send.encode())
    except (KeyboardInterrupt, ConnectionResetError):
        break

client.close()
