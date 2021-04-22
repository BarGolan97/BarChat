
import socket
import time

def interact(sock):
     command=''
     while(command != 'exit'):
         command=input('$ ')
         sock.send(command + '\n')
         time.sleep(.5)
         print( sock.recv(0x10000))
     return

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', 9999))
s.listen(5)

interact(s.accept())
