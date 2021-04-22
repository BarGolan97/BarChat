import socket

address = '127.0.0.1'

port = 8000
bsize = 1024
import time
import random
clientSocket = socket.socket()
clientSocket.connect((address, port))

userName=input('please Enter your name\n')
running=True

while running:
    disconnect=False
    msg = 'start,' + userName
    clientSocket.send(msg.encode())
    print (msg)
    time.sleep(1)
    msg=clientSocket.recv(bsize)
    print (msg.decode('utf8'))
    n=random.randint(100,500)
    for i in range(n):
        clientSocket.send(str(i).encode())
        data = clientSocket.recv(bsize)
        print( data.decode('utf8'))

        time.sleep(0.5)

    running=False
