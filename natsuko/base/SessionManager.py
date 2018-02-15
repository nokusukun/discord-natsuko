import json
import pickle

class SessionManager():

	def __init__(self, _session):
		print("SMAN({})".format(_session))
		self._file = _session
		self._session = {}
		try:
			with open(self._file) as f:
				self._session = json.loads(f.read())
		except:
			pass

	def __setattr__(self, attr, val):
		try:
			if attr != "_session":
				self._session[attr] = val
				with open(self._file, "w") as f:
					f.write(json.dumps(self._session))
				return None
		except:
			pass
		super().__setattr__(attr, val)



	def __getattr__(self, attr):
		try:
			# Why does it read? Idk, probably when it gets modified by 
			# 	a different application on runtime.
			if attr != "_session":
				with open(self._file) as f:
					self._session = json.loads(f.read())
				return self._session[attr]
		except:
			pass
			
		return None


class BinarySessionManager():

	def __init__(self, _session):
		self._file = _session
		self._session = {}
		try:
			with open(self._file, "rb") as f:
				self._session = pickle.load(f)
		except:
			pass

	def save(self):
		with open(self._file, "wb") as f:
			pickle.dump(self._session, f)

	def __setattr__(self, attr, val):
		try:
			if attr != "_session":
				self._session[attr] = val
				with open(self._file, "wb") as f:
					pickle.dump(self._session, f)
				return None
		except:
			pass
		super().__setattr__(attr, val)



	def __getattr__(self, attr):
		try:
			# Why does it read? Idk, probably when it gets modified by 
			# 	a different application on runtime.
			if attr != "_session":
				#with open(self._file, "rb") as f:
				#	self._session = pickle.load(f)
				return self._session[attr]
		except:
			pass
			
		return super().__getattr__(attr)