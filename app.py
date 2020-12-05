# -*- coding: utf-8 -*-
from flask import Flask, render_template, url_for, redirect
from flask import request as flaskRequest
import json, datetime, dateparser, string
from db_controller import DB

app = Flask(__name__)

db = DB("165.22.193.119", 27017, "root", "toor")

categories = ['Mugging', 'Break-in']


def format_date(userdate):
    date = dateparser.parse(userdate)
    try:
        return datetime.datetime.strftime(date, "%Y-%m-%d")
    except:
        return None


def sanitize_string(userinput):
    whitelist = string.ascii_letters + string.digits + " !?$.,;:-'()&\""
    return ''.join(list(filter(lambda x: x in whitelist, userinput)))


@app.route("/")
def index(error_message=None):
    events = json.dumps(DB.get_all_events())
    return render_template('index.html', crimes=events,
                           categories=categories, error_message=error_message)


@app.route("/get_events", methods=["GET"])
def get_events():
    if flaskRequest.args.get('lvl') and flaskRequest.args.get('lvl').isnumeric():
        lvl = flaskRequest.args.get('lvl')
        data = json.dumps(db.get_events_by_lvl(int(lvl)))
    else:
        data = json.dumps(db.get_all_events())
    return data

# доделать после auth
@app.route("/update_event", methods=["POST"])
def update_events():
    data = flaskRequest.get_json()
    try:
        _id = data["_id"]
        new_d = data["new_data"]
        db.update_event(_id=_id, new_d=new_d)
        return json.dumps({"success": True})
    except KeyError:
        return json.dumps({"error": "Missing arguments"})


@app.route("/remove_event", methods=["GET"])
def remove_event():
    if flaskRequest.args.get('_id') and flaskRequest.args.get('_id').isnumeric():
        _id = flaskRequest.args.get('_id')
        data = json.dumps(db.remove_event(int(_id)))
    else:
        data = json.dumps({"error": "Missing arguments"})
    return data


@app.route("/insert_event", methods=["POST"])
def insert_event():
    data = flaskRequest.get_json()
    try:
        title = data["title"]
        desc = data["desc"]
        img = data["img"]
        lvl = int(data["lvl"])
        lon = data["lon"]
        lat = data["lat"]
        if lvl == 1:
            cnfrmd = True
        else:
            cnfrmd = False
        db.insert_event(title=title, desc=desc, img=img, lvl=lvl, lon=lon, lat=lat, cnfrmd=cnfrmd)
        return json.dumps(data)
    except KeyError:
        return json.dumps({"error": "Missing arguments"})
    


@app.route("/add", methods=["POST"])
def add():
    category = flaskRequest.form.get('category')
    if category not in categories:
        return redirect(url_for('index'))
    title = flaskRequest.form.get('title')
    #date = format_date(flaskRequest.form.get('date'))
    #if not date:
    #    return index("Invalid date. Please use dd-mm-YYYY format")
    try:
        latitude = float(flaskRequest.form.get('latitude'))
        longitude = float(flaskRequest.form.get('longitude'))
    except ValueError:
        return index("Please place marker on the map")
    description = sanitize_string(flaskRequest.form.get('description'))
    try:
        DB.add_event(category, title, latitude, longitude, description)
    except Exception as e:
        print(e)
    finally:
        return index()


@app.route("/auth", methods=["GET", "POST"])
def auth():
    pass


if __name__ == "__main__":
    app.run(debug=True)
