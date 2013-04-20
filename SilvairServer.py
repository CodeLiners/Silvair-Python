from Exceptions import ConnectException
from threading import Thread
from ClientConnection import ClientCon
import socket

class Server:
    """The class for an IRC Server"""
    def __init__(self, bind, port):
        if bind is None:
            bind = ""
        self.port = port
        self.bind = bind
        self.isListening = False
        self._sock = None

    def _listen(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self._sock.bind((self.bind, self.port)) 
        self._sock.listen(1)
        try:
            while True:
                con, addr = self._sock.accept()
                ClientCon(con, addr)
        except Exception, ex:
            raise ex
        finally:
            self._sock.close()

    def listen(self):
        if self.isListening:
            raise ConnectException("already listening")
        self.isListening = True;
        Thread(target = self._listen).start()
        