from pymongo import MongoClient
import time, bcrypt, hashlib

class DB:
	def __init__(self, addr, port, user, pwd):
		self.addr = addr
		self.port = port
		self.user = user
		self.pwd = pwd
		self.client = MongoClient("mongodb://%s:%s@%s" % (user, pwd, addr))
		self.events = self.client.test["events"]
		self.users = self.client.test["users"]

	def add_user(self, name:str, phone:str, hpwd:str):
		return self.users.insert_one({
			"name": name,
			"phone": phone,
			"hpwd": hpwd,
			"role": "user",
			"events": []
			}).inserted_id

	def update_user_token(self, phone):
		token = phone+ str(time.time()) + phone * 2 + str(time.time())
		token = hashlib.sha256(token.encode("utf-8")).digest().hex()
		return self.users.update(
			{"phone": phone}, 
			{"token": token, "creation_date" : int(time.time())}, upsert=True)

	def get_user(self, phone):
		return self.users.find_one({"phone" : phone})

	def get_all_events(self):
		return list(self.events.find({}, {'_id': False}).sort([['_id', 1]]))

	def get_event_by_id(self, _id:int):
		return list(self.events.find({}, {'_id': False}).sort([['_id', 1]]).skip(_id-1).limit(1))[0]

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

	def update_event(self, _id:int, new_d:dict):
		_id -= 1

		events = list(self.events.find({}).sort([['_id', 1]]))
		return self.events.update_one(
			{'_id': events[_id]["_id"]},
			{'$set': new_d }, upsert=False).modified_count


	def remove_event(self, _id:int):
		_id -= 1

		events = list(self.events.find({}).sort([['_id', 1]]))
		return self.events.delete_one({"_id" : events[_id]["_id"]}).deleted_count

