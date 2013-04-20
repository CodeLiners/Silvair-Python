from Hooks import callHook
from Utils import Struct
from threading import Thread

class ClientCon:
	"""docstring for ClientCon"""
	def __init__(self, con, addr):
		self.con = con
		self.file = con.makefile()
		self.addr = addr
		self.user = None
		self.sentpass = false
		self._hooks = []
		Thread(target = self._listen).start()

	def _listen(self):
		callHook("newClient", self)
		while True:
			line = self.file.readline()
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
			t = line.split(" :")
			data.argline = t[0]
			data.args = data.argline.split()
			if len(t) > 1:
				data.data = line[len(data.argline) + 2:]
			else:
				data.data = None
			data.passthough = True
			self._callHook("in_DATA_" + data.args[0].upper(), data)
			if data.passthough and not self.user is None:
				self.user.sendToServer(args = data.args, data = data.data)

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
			self.file.write(line + "\r\n")

	def send(self, args = [], data = None, prefix = None):
		if prefix is None:
			prefix = ":"
		else:
			prefix += ":"
		argline = " ".join(args)
		if data is None:
			data = ""
		else:
			data = " :" + data
		self.sendLine(prefix + argline + data)