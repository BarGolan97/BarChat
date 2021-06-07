import socket
import threading
import queue
import time
import os


MY_PROCESS = 0
MY_USERNAME = 1
MY_SOCKET = 2
OTHER_PLAYER = 3
OTHER_SOCKET = 4
outgoingQ = queue.Queue()


class ThreadedServer(threading.Thread):
    def __init__(self, host, port, q):
        super(ThreadedServer, self).__init__()
        self.plist = []
        self.pairlist = []
        self.host = host
        self.port = port
        self.q = q
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

        self.sock.listen(10)
        p = sendToClient(self.q)
        p.start()
        # self.plist.append(p)

    def run(self):
        while True:
            client, address = self.sock.accept()
            client.settimeout(60)
            p = listenToClient(client, address, self.plist, self.q)

            self.plist.append([p, 'MyUserName', client, 'waiting', 'otherSocket'])

            p.start()


class listenToClient(threading.Thread):
    def __init__(self, client, addres, plist, q):
        super(listenToClient, self).__init__()
        self.client = client
        self.adress = addres
        self.plist = plist
        self.size = 1024
        self.q = q
        self.p=[MY_PROCESS,MY_USERNAME,MY_SOCKET,'waiting',OTHER_SOCKET]

        self.playing = False
        self.running=True
    def run(self):
        print( 'runnung ', self.adress)
        # update local record of process and socket in global plist
        for p in self.plist:

            if p[MY_SOCKET] == self.client:
                self.p[MY_PROCESS] = p[MY_PROCESS]
                self.p[MY_SOCKET]=self.client
                self.p[OTHER_PLAYER]='waiting'
                print ('listenToClient update plist ',self.p)
        while self.running:
            try:
                self.data = self.client.recv(self.size)
                self.data=self.data.decode('utf8')
            except:
                for p in self.plist:  #KILL CLIENT

                    if p[MY_SOCKET] == self.client:
                        self.plist.remove(p)
                self.running=False

            if self.data:
                msg = self.data.split(',')

                if msg[0] == 'start':  # register player

                    self.userName = msg[1]
                    print (self.userName)
                    for p in self.plist:  #update locl record and global record adding user name and 'waiting' means no partner yet
                        if p[MY_PROCESS] == self.p[MY_PROCESS]:
                            self.p[MY_USERNAME]=self.userName
                            self.p[OTHER_PLAYER] = 'waiting'
                            p[MY_USERNAME] = self.userName
                            p[OTHER_PLAYER] = 'waiting'
                            print (p)
                            print ('new user' ,self.p)
                    for p1 in self.plist: # find process record in list so we can find a partner
                        if p1[MY_PROCESS]==self.p[MY_PROCESS]:
                            break
                        print (p1)
                    print (self.plist)
                    for p2 in self.plist: # find candidate playmate

                        if p2[MY_PROCESS] is not self.p[MY_PROCESS]:
                            print('looking for partner')
                            print( p2[MY_PROCESS],"p2")
                            print (self.p[MY_PROCESS],'self.p')
                            if p2[OTHER_PLAYER] == 'waiting':
                                self.connectPlayers(p1,p2)


                    if not self.playing:
                        print('check if player left game')
                        self.updatePlayStatus()

                    print (str(self.p[MY_USERNAME])+'  start playng with ' + str(self.p[OTHER_PLAYER]))
                    response = str(self.p[MY_USERNAME])+"  Playing with" + ' : ' + str(self.p[OTHER_PLAYER])
                    msgToSend = [self.p[OTHER_SOCKET], response]
                    print(response)
                    self.q.put(msgToSend)
                    msgToSend = [self.p[MY_SOCKET], response]
                    self.q.put(msgToSend)
                    self.gameApp()
                else:
                    if self.playing:
                        print ('performing game app',p)
                        self.gameApp()
            else:
                print ('closing')
                self.client.close()


    def connectPlayers(self,p1, p2):
        print ('connect players ')
        self.p[OTHER_PLAYER] = p2[MY_USERNAME]
        self.p[OTHER_SOCKET] = p2[MY_SOCKET]
        p1[OTHER_PLAYER] = p2[MY_USERNAME]
        p1[OTHER_SOCKET] = p2[MY_SOCKET]
        p2[OTHER_PLAYER] = self.p[MY_USERNAME]
        p2[OTHER_SOCKET] = self.p[MY_SOCKET]
        os.system('python clientwhatsapp.py')


    def updatePlayStatus (self):
        running=True
        while running:
            for p in self.plist:
                if self.p[MY_PROCESS]==p[MY_PROCESS]:
                    if p[OTHER_PLAYER] != 'waiting':
                        self.p[OTHER_PLAYER]=p[OTHER_PLAYER]
                        self.p[OTHER_SOCKET] = p[OTHER_SOCKET]
                        self.playing = True
                        running=False
                        print (self.p ,'playstatus')
                        print (p)
                        break
                time.sleep(0.3)

    def gameApp(self):
        print ('hello')
        # Set the response to echo back the recieved data
        response = str(self.p[MY_USERNAME]) + ' : ' + self.data
        msgToSend = [self.p[OTHER_SOCKET], response]
        # self.client.send(response)
        self.q.put(msgToSend)
        time.sleep(0.2)


class sendToClient(threading.Thread):
    def __init__(self, q):
        super(sendToClient, self).__init__()

        self.size = 1024
        self.q = q

    def run(self):
        print ('start send process')
        while True:

            if not self.q.empty():
                message = self.q.get()
                try:
                    message[0].send(message[1].encode())
                except:
                    print ('socket error :',message[0],message[1])

            time.sleep(0.1)


if __name__ == "__main__":
    port_num = 8001
    Ts = ThreadedServer('0.0.0.0', port_num, outgoingQ)
    Ts.start()
    Ts.join()