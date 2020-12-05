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
		return list(self.events.find({}, {'_id': False}))

	def insert_events(self, title:str, desc:str, img:str, lvl:int, lon:float, lat:float, cnfrmd:bool):
		return self.events.insert_one({
			"title": title,
			"desc": desc,
			"img": img,
			"lvl": lvl,
			"lon": lon,

			})
	
	def get_events_by_level(self, lvl:int):
		pass

	def update_event(self, id:int, new:dict):
		pass

	def remove_event(self, id:int):
		pass

