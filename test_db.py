from db_controller import DB

db = DB("localhost", "27017", "root", "toor")
print(db.get_all_crimes())