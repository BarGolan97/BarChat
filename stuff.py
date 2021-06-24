class EchoServerFactory(protocol.ClientFactory):
   protocol  = EchoProtocol
   clients = []
   groups = {}

def dataReceived(self, data):
   # Split string ,error checking ...
   if command == "join":
      self.factory.groups.get(content, []).append(self)
   # handle other commands

def sendMsg(self, message, group):
   for client in self.factory.groups[group]:
      client.transport.write( message + '\n')



      client_socket.send(bytes("$$$i want to know the groups", "utf8"))

      list_of_groups = client_socket.recv(BUFSIZ)
      list_of_groups = pickle.loads(list_of_groups)