import os
from venv import create
from flask import Flask, render_template, request
from dotenv import load_dotenv
from peewee import *
import datetime
from playhouse.shortcuts import model_to_dict 

load_dotenv()
app = Flask(__name__)
if os.getenv("TESTING") == "true":
    print("Running in test mode")
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared', uri=True)
else:
    mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"),user=os.getenv("MYSQL_USER"), password=os.getenv("MYSQL_PASSWORD"), host=os.getenv("MYSQL_HOST"), port=3306)
    print(mydb)

@app.route('/')
def index():
    return render_template('index.html', title="MLH Fellow", url=os.getenv("URL"))

@app.route('/aboutMe')
def aboutMe():
    return render_template('about_me.html', title="About Me")

@app.route('/experience')
def experience():
    return render_template('experience.html', title="Experience")

@app.route('/travel')
def travel():
    return render_template('travel.html', title="My Travels")

@app.route('/hobbies')
def hobbies():
    return render_template('hobbies.html', title="Hobbies")

@app.route('/education')
def education():
    return render_template('education.html', title="Edcaction")

@app.route('/timeline')
def timeline():
    return render_template('timeline.html', title='Timeline')


class TimelinePost(Model):
    date = CharField()
    title = CharField()
    events = TextField()

    class Meta:
        database = mydb

mydb.connect()
mydb.create_tables([TimelinePost])

@app.route("/api/timeline_post", methods=["GET", "POST", "DELETE"])
def timeline_post():
    if request.method == "POST":
        try:
            date = request.form['date']
        except KeyError:
            return "Invalid Date", 400

        try:
            title = request.form['title']
        except KeyError:
            return "Invalid Title", 400

        try:
            events = request.form['events']
            if len(events) < 1:
                return "Invalid Body", 400
        except KeyError:
            return "Invalid Body", 400

        timeline_post = TimelinePost.create(date=date,
                                            title=title,
                                            events=events)

        return model_to_dict(timeline_post)

    if request.method == "GET":
        return {'posts': [model_to_dict(p) for p in TimelinePost.select()]}

    elif request.method == "DELETE":
        del_id = request.form["id"]
        TimelinePost.delete_by_id(del_id)
        return f'Removed ID: {del_id}'
    

