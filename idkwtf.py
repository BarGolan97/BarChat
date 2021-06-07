from twisted.internet import reactor,protocol
from twisted.protocols import basic
from twisted.internet.protocol import Protocol, ClientFactory
import time

def t():

return ("["+ time.strftime("%H:%M:%S") +"] ")

class EchoProtocol(basic.LineReceiver):
  name = "Unnamed"

  def connectionMade(self):

    self.transport.write("WhiteNOISE"+"\n")
    self.sendLine("Enter A name Below...")
    self.sendLine("")
    self.count = 0
    self.factory.clients.append(self)
    self.factory.group.append(self)
    print t() + "+ Connection from: "+ self.transport.getPeer().host

  def connectionLost(self, reason):

    self.sendMsg("- %s left." % self.name)
    print t() + "- Connection lost: "+ self.name
    self.factory.clients.remove(self)
  def dataReceived(self, data):
        #print "data is ", data
            a = data.split(':')
            if len(a) > 1:
                    command = a[0]
                    content = a[1]


                    msg = ""
                    if command == "iam":
                            self.name = content
                            msg = self.name + " has joined"

                    elif command == "msg":
                            msg = self.name + ": " + content
                    elif command  == "quit":
                            self.transport.loseConnection()
                            return
                    elif command == "/ul":
                            self.chatters()
                            return()

                    print msg
                    self.sendMsg(msg)

  def username(self, line):

    for x in self.factory.clients:
        if x.name == line:
            self.sendLine("This username is taken; please choose another")
            return

    self.name = line
    self.chatters()
    self.sendLine("You have been connected!")
    self.sendLine("")
    self.count += 1
    self.sendMsg("+ %s joined." % self.name)
    print '%s~ %s connected as: %s' % (t(), self.transport.getPeer().host, self.name)

  def chatters(self):
    x = len(self.factory.clients) - 1
    s = 'is' if x == 1 else 'are'
    p = 'person' if x == 1 else 'people'
    self.sendLine("There %s %i other %s connected:" % (s, x, p) )

    for client in self.factory.clients:
        if client is not self:
            self.sendLine(client.name)
    self.sendLine("")

  def sendMsg(self, message):

    for client in self.factory.clients:
        client.transport.write( message + '\n')



class EchoServerFactory(protocol.ClientFactory):
protocol  = EchoProtocol
clients = []

if __name__ == "__main__":
reactor.listenTCP(5001, EchoServerFactory())
print ("Chat Server Started")
reactor.run()