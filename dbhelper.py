# -*- coding: utf-8 -*-
import sqlite3
import datetime


class DBHelper:

    def connect(self):
        connection = sqlite3.connect('events.db')
        return connection

    def get_all_events(self):
        connection = self.connect()
        try:
            query = "SELECT * FROM events;"
            cursor = connection.cursor()
            cursor.execute(query)
            json_events = []
            for event in cursor:
                json_events.append({
                    'id': event[0],
                    'category': event[1],
                    'title': event[2],
                    'latitude': event[3],
                    'longitude': event[4],
                    'description': event[5]
                })
            return json_events
        finally:
            connection.close()

    def add_event(self, category, title, latitude, longitude, description):
        connection = self.connect()
        try:
            query = "INSERT INTO events (category,title,latitude,longitude,description) VALUES (%s, %s, %s, %s, %s);"
            cursor = connection.cursor()
            cursor.execute(query, (category, title, latitude, longitude, description))
            connection.commit()
        except Exception as e:
            print(e)
        finally:
            connection.close()
