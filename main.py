#!/usr/bin/python
from SilvairServer import Server
from Hooks import *
from User import User
import Core
import hashlib

Core.setup()

mainserv = Server(None, 8001)
mainserv.listen();

s = hashlib.sha512()
s.update("test")
passw = s.hexdigest()

serv = {"host": "irc.esper.net", "port": 6667, "pass": None}
user = {"name": "Kilobyte", "pass": passw, "server": serv, "nick": "Kilo2", "realname": "Test", "ident": "test"}
User(user)