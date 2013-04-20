from ServerConnection import ServerCon
import socket

class User:
    """User class"""
    def __init__(self, data):
        self.data = data
        self.nick = data['nick']
        self.clients = []
        self.connectToServer()

    def sendLineToServer(self, line):
        self.servcon.sendLine(line)

    def sendToServer(self, *d, **data):
        self.servcon.send(*d, **data)

    def broadcastLineToClients(self, line):
        for client in self.clients:
            client.sendLine(line)

    def broadcastToClients(self, *d, **data):
        for client in self.clients:
            client.send(*d, **data)

    def setNick(self, nick):
        self.sendToServer(args = ["NICK", nick])

    def connectToServer(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        sock.connect((self.data['server']['host'], self.data['server']['port']))
        self.servcon = ServerCon(sock, self.data['server'], self)