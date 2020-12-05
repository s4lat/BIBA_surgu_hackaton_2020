import sqlite3
import os

dbpath = "events.db"
if not os.path.exists(dbpath):
    open(dbpath, 'w').close()
'''
connection = pymysql.connect(host='localhost',
                             user=dbconfig.db_user,
                             password=dbconfig.db_password)'''

connection = sqlite3.connect('events.db')
try:
    cursor = connection.cursor()
    # sql = "CREATE DATABASE IF NOT EXISTS biba"
    # cursor.execute(sql)
    sql = """CREATE TABLE IF NOT EXISTS events (
	id	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	title	TEXT NOT NULL,
	category	TEXT NOT NULL,
	latitude	REAL NOT NULL,
	longitude	REAL NOT NULL,
	description	TEXT NOT NULL );
"""
    cursor.executescript(sql)
    connection.commit()
finally:
    connection.close()
