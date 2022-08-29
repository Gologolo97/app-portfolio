import os
from flask import Flask, redirect, url_for, request, render_template
from pymongo import MongoClient


app = Flask("DockerTutorial")

#Hi
#mongodb_host = os.environ.get('MONGO_HOST', 'MONGODB_URI')
#mongodb_port = int(os.environ.get('MONGO_PORT', '27017'))
MONGODB_URI = os.environ['MONGODB_URI']
client = MongoClient(MONGODB_URI)
#db = client.appdb
mydb = client["mydatabase"]
db = mydb["notes"]


@app.route("/")
def index():
   # _items = db.appdb.find()
    _items = db.find()
    items = [items for items in _items]

    return render_template("index.html", items=items)


@app.route("/new", methods=["POST"])
def new():
    data = {
        "helloworld": request.form["helloworld"]
    }

    #db.appdb.insert_one(data)
    db.insert_one(data)

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

