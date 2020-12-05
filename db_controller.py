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
		return list(self.events.find({}, {'_id': False}).sort([['_id', 1]]))

	def insert_event(self, title:str, desc:str, img:str, lvl:int, lon:float, lat:float, cnfrmd:bool):
		return self.events.insert_one({
			"title": title,
			"desc": desc,
			"img": img,
			"lvl": lvl,
			"lon": lon,
			"lat": lat,
			"confirmed": cnfrmd
			}).inserted_id
	
	def get_events_by_lvl(self, lvl:int):
		return list(self.events.find({"lvl" : lvl}, {'_id': False}))

	def update_event(self, id:int, new:dict):
		pass

	def remove_event(self, _id:int):
		events = list(self.events.find({}).sort([['_id', 1]]))
		return self.events.delete_one({"_id" : events[_id-1]["_id"]}).deleted_count

