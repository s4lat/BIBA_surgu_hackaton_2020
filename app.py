# -*- coding: utf-8 -*-

from flask import Flask, render_template, url_for, redirect, make_response
from flask import request as flaskRequest
from db_controller import DB
import json, time

app = Flask(__name__)

db = DB("165.22.193.119", 27017, "root", "toor")
TOKEN_LIFETIME = 21600

def is_user_authenticated():
    auf = flaskRequest.cookies.get("auf")
    if not auf:
        return False
    phone, token = auf.split(":")
    user = db.get_user(phone)

    if not user:
        return False
    if time.time() - user["creation_date"] > TOKEN_LIFETIME:
        return False
    if token != user["token"]:
        return False

    return True


def auth_required(func):
    def wrapper():
        if is_user_authenticated():
            return func()
        else:
            return redirect("/auth")

    return wrapper


@app.route("/")
@auth_required
def index():
    events = json.dumps(db.get_all_events())
    return "SDASFSFSDGDTJUYWSDXC"


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


@app.route("/auth", methods=["GET", "POST"])
def auth():
    return "Авторизуйся дядя"

@app.route("/reg", methods=["GET", "POST"])
def reg():
    data = flaskRequest.get_json()

    return render_template("register.html")


if __name__ == "__main__":
    app.run(debug=True)
