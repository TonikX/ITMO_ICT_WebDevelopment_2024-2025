import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 1236))


a = input("Enter the first number: ")
b = input("Enter the second number: ")
nums = [a, b]
for num in nums:
    s.send(num.encode('utf-8'))

msg = s.recv(1024)
umsg = msg.decode('utf-8')
print(umsg)
s.close()



