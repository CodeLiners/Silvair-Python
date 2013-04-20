from Hooks import callHook
from Utils import Struct, sendLineToSocket
from threading import Thread

class ServerCon:
    """docstring for ServerCon"""
    def __init__(self, con, serv, user):
        self.con = con
        self.file = con.makefile()
        self.user = user
        self.serv = serv
        self._hooks = []
        self._loggedin = False
        Thread(target = self._listen).start()

    def _listen(self):
        callHook("newServer", self)
        while True:
            line = self.file.readline().replace("\n", "").replace("\r", "")
            if not self._loggedin:
                self._login()
                self._loggedin = True
            if line == "":
                self._callHook("disconnect", None)
                return
            data = Struct()
            data.line = line
            data.con = self
            data.passthough = True
            self._callHook("in_raw", data)
            if not data.passthough: # a module requested to not pass the command
                continue
            data = Struct()
            t = line.split(":")
            data.prefix = t[0]

            t = line[len(data.prefix) + 1:].split(" :")
            data.argline = t[0]
            data.args = data.argline.split()
            if len(t) > 1:
                data.data = line[len(data.argline) + 2:]
            else:
                data.data = None
            data.passthough = True
            self._callHook("in_DATA_" + data.args[1].upper(), data)
            if data.passthough:
                self.user.broadcastToClients(args = data.args, data = data.data, prefix = data.prefix)

    def _login(self):
        if not self.serv['pass'] is None:
            self.send(args = ["PASS", self.serv['pass']])
        self.send(args = ["NICK", self.user.nick], data = None)
        self.send(args = ["USER", self.user.data['ident'], "0", self.serv['host']], data = self.user.data['realname'])

    def _callHook(self, name, data):
        for hook in self._hooks:
            if name in hook:
                hook[name](data)

    def regHook(self, handler):
        self._hooks.append(handler)

    def sendLine(self, line):
        data = Struct()
        data.con = self
        data.passthough = True
        data.line = line
        self._callHook("out_raw", data)
        if data.passthough:
            sendLineToSocket(self.con, line + "\r\n")

    def send(self, args = [], data = None):
        argline = " ".join(args)
        if data is None:
            data = ""
        else:
            data = " :" + data
        self.sendLine(argline + data)