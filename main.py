#!/usr/bin/python
from SilvairServer import Server
from Hooks import *
from User import User
import Core
from Logging import log, Level
import hashlib

Core.setup()

log(Level.INFO, "Starting server...")
mainserv = Server(None, 8001)
mainserv.listen();
log(Level.INFO, "Done")

s = hashlib.sha512()
s.update("test")
passw = s.hexdigest()

serv = {"host": "localhost", "port": 6667, "pass": None}
user = {"name": "Kilobyte", "pass": passw, "server": serv, "nick": "Kilo2", "realname": "Test", "ident": "test"}
User(user)