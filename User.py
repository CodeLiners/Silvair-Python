from ServerConnection import ServerCon
from Logging import *
import socket

class User:
    """User class"""
    def __init__(self, data):
        log(Level.DEBUG, "Created user: " + data['name'])
        self.data = data
        self.nick = data['nick']
        self.clients = []
        self.channels = []
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
        log(Level.DEBUG, "[" + self.data['name'] + "] Connecting...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        sock.connect((self.data['server']['host'], self.data['server']['port']))
        log(Level.DEBUG, "Done...")
        self.servcon = ServerCon(sock, self.data['server'], self)

    def getMask(self):
        return self.nick + "!" + self.ident + "@" + self.hostmask

    def introduceClient(self, client):
        for c in self.channels:
            client.send(args = [self.getMask(), "JOIN", ])