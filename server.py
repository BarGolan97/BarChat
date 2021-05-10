"""Server for multithreaded (asynchronous) chat application."""
import time
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import pickle

def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""

    someMsg = client.recv(BUFSIZ)
    someMsg = pickle.loads(someMsg)

    while someMsg[0] == 'register' :

        print(someMsg[0], someMsg[1], someMsg[2], 'hellllllllooooooo')
        name = someMsg [1]
        password_info = someMsg [2]
        file = open('UserDataBase.txt', "a")
        file.write(name + "-")
        file.write(password_info + '\n')
        file.close()
        someMsg = client.recv(BUFSIZ)
        someMsg = pickle.loads(someMsg)




    if someMsg[0] == 'signin' :

        print(someMsg[0], someMsg[1], someMsg[2], 'hiosh')

        name = someMsg[1]
        password1 = someMsg [2]


        file1 = open("UserDataBase.txt", "r")
        PwordandUsername = file1.read().splitlines()

        if name + '-' + password1 in PwordandUsername:
            Dindex = PwordandUsername.index(name + '-' + password1)
            Userinfo = PwordandUsername[Dindex]
            a = Userinfo.split('-')
            Pword = str(a[1])
            global Username
            Username = str(a[0])

            if password1 == Pword and name == Username:
                print('im in!')
                client.send(bytes("login success", "utf8"))


            elif password1 != Pword:
                client.send(bytes("login fail", "utf8"))

        else:
            client.send(bytes("login fail", "utf8"))

    time.sleep(1)
    welcome = '\nWelcome %s! If you ever want to quit, type {quit} to exit.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat!" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name

    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"):
            broadcast(msg, name + ": ")
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            break


def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""

    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg)


clients = {}
addresses = {}

HOST = ''
PORT = 33000 #33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()