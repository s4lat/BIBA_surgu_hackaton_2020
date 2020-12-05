from pymongo import MongoClient

class DB:
	def __init__(self, addr, port, user, pwd):
		self.addr = addr
		self.port = port
		self.user = user
		self.pwd = pwd
		self.client = MongoClient("mongodb://%s:%s@%s" % (user, pwd, addr))
		self.events = self.client.test["events"]

	def get_all_events(self):
		return list(self.events.find({}))

	def insert_events(self, id:int, title:str, desc:str, img:str, lvl:int, lon:float, lat:float, cnfrmd:bool):
		pass
	
	def get_events_by_level(self, lvl:int):
		pass

	def update_event(self, id:int, new:dict):
		pass

	def remove_event(self, id:int):
		pass

