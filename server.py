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

    people_in_group = []



    someMsg = client.recv(BUFSIZ)
    someMsg = pickle.loads(someMsg)

    while someMsg[0] == 'register' :


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

                client.send(bytes("login success", "utf8"))


            elif password1 != Pword:
                client.send(bytes("login fail", "utf8"))
                client.close()
                del clients[client]

        else:
            client.send(bytes("login fail", "utf8"))
            client.close()
            del clients[client]


    time.sleep(1)
    welcome = '\nWelcome %s! \n If you ever want to quit,type {quit} to exit.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat!" % name
    #broadcast(bytes(msg, "utf8"), 'placeholder')
    clients[client] = name

    while True:

        msg = client.recv(BUFSIZ)
        decodedMSG = msg.decode("utf8")

        if decodedMSG[0] == "#" :
            '''
            try:

                list_of_groups[G].remove(client)
                G = decodedMSG[1:]

                if G in list_of_groups.keys():

                    uhhh = list_of_groups[G]
                    uhhh.append(client)
                    list_of_groups[G] = uhhh
                    print(list_of_groups)


                else:
                    people_in_group.append(client)
                    list_of_groups[G] = people_in_group
                    people_in_group = []

                    for this in list_of_groups.keys():
                        actually[this] = []



                print('im in')
                print(list_of_groups)

            
#-----------------------------------------------------------_#

            except:
'''
            G = decodedMSG[1:]
            if G in list_of_groups.keys():

                uhhh = list_of_groups[G]
                if client not in uhhh:
                    uhhh.append(client)
                list_of_groups[G] = uhhh
                print(list_of_groups)


            else:
                people_in_group.append(client)
                list_of_groups[G] = people_in_group
                people_in_group = []

                for this in list_of_groups.keys():
                    actually[this] = []

                file_to_read = open("/Users/bargolan/PycharmProjects/if/cyberfinal_project/group_dic.pickle", "ab")
                dumped_dictionary = pickle.dump(actually, file_to_read, protocol=pickle.HIGHEST_PROTOCOL)

            print('im in')
            print(list_of_groups)




            '''file = open("UserDataBase.txt", "r")
            PwordandUsername = file.read().splitlines()

            if name + '-' + password1 in PwordandUsername:
                Dindex = PwordandUsername.index(name + '-' + password1)
                data = file.readlines()
                data[Dindex] += "-"+G+'\n'
                file = open('UserDataBase.txt', "w")
                file.writelines(data)
                file.close() '''

        elif decodedMSG == "$$$i want to know the groups":
            th = []
            for var in list_of_groups.keys():
                th.append(var)

            data_string = pickle.dumps(th)
            client.send(data_string)


        elif decodedMSG == "{quit group}":
            list_of_groups[G].remove(client)
            broadcast(bytes("%s has left the chat." % name, "utf8"),G)




        elif msg != bytes("{quit}", "utf8"):
            print('I WANT TO BROADCAST A THING\n\n')
            broadcast(msg, G ,name + ": ")

        else:
            #Gets client out of group if leaves
            client.send(bytes("{quit}", "utf8"))
            list_of_groups[G].remove(client)
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat." % name, "utf8"),G)
            break


def broadcast(msg, group, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""
    #msg = msg+'|'+ group
    people = list_of_groups[group]
    print (people)
    print('LIST OF GROUPS : \n'+str(list_of_groups))
    the_msg =bytes(prefix, "utf8") + msg+ bytes('|'+group,'utf8')
    print (the_msg)
    for sock in people :
        print ('im sending somthing to this persone' + str (sock))
        sock.send(the_msg)

    #for sock in group
    #do bla bla bla


clients = {}
addresses = {}
actually = {}
flik = open("/Users/bargolan/PycharmProjects/if/cyberfinal_project/" + "group_dic.pickle","rb")
loadrded = pickle.load(flik)
list_of_groups = loadrded
print (list_of_groups)


HOST = ''
PORT = 32000 #33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":

    SERVER.listen(6)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()

    #