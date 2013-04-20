from Hooks import regHook
from Logging import log
import User
import hashlib

def universalRaw(arg):
    line = arg.line
    if line.upper()[:6] == "PING :":
        arg.con.sendLine("PONG :" + line[6:])
        arg.passthough = False # don't send to server/client

def clientUSER(arg):
    if arg.con.pw is None:
        arg.con.sendLine(":Silvair!bnc@codeliners.org 464 :You need to send a password (user:pass) before sending the USER command")
        arg.con.close()
        arg.passthough = False
    else:
        if arg.con.user is None:
            arg.passthough = False
            p = arg.con.pw.split(":")
            if len(p) != 2:
                arg.con.sendLine(":Silvair!bnc@codeliners.org 464 :Invalid server password format")
                arg.con.close()
                return
            user = User.resolve([0])
            if user is None:
                arg.con.sendLine(":Silvair!bnc@codeliners.org 464 :Invalid user credentials")
                arg.con.close()
                return
            h = hashlib.sha512()
            h.update(p[1])
            if user.data['pass'] != h.hexdigest():
                arg.con.sendLine(":Silvair!bnc@codeliners.org 464 :Invalid user credentials")
                arg.con.close()
                return
            con.user = user

### CLIENT ###

def clientPASS(arg):
    arg.con.pw = arg.args[1]

def clientInRaw(arg):
    log(1, "[CLIENT] -> [BNC] " + arg.line)

def clientOutRaw(arg):
    log(1, "[CLIENT] <- [BNC] " + arg.line)

### SERVER ###

def serverInRaw(arg):
    log(1, "[BNC] <- [IRCD] " + arg.line)

def serverOutRaw(arg):
    log(1, "[BNC] -> [IRCD] " + arg.line)

def serverNICK(arg):
    arg.con.user.nick = arg.args[2]

### GENERAL ###

def newClient(client):
    client.regHook({"in_raw": universalRaw})
    client.regHook({"in_raw": clientInRaw, "out_raw": clientOutRaw})

def newServer(server):
    server.regHook({"in_raw": universalRaw})
    server.regHook({"in_raw": serverInRaw, "out_raw": serverOutRaw})

def setup():
    regHook("newClient", newClient)
    regHook("newServer", newServer)