class Struct:
    """A simple empy class intended to be used a data structure"""

def sendLineToSocket(sock, line):
    totalsent = 0
    MSGLEN = len(line)
    while totalsent < MSGLEN:
        sent = sock.send(line[totalsent:])
        if sent == 0:
            raise RuntimeError("socket connection broken")
        totalsent = totalsent + sent