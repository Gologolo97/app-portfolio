import os
from flask import Flask, redirect, url_for, request, render_template
from pymongo import MongoClient


app = Flask("DockerTutorial")

mongodb_host = os.environ.get('MONGO_HOST', 'mongo')
mongodb_port = int(os.environ.get('MONGO_PORT', '27017'))

client = MongoClient(mongodb_host, mongodb_port)
db = client.appdb

@app.route("/")
def index():
    _items = db.appdb.find()
    items = [items for items in _items]

    return render_template("index.html", items=items)


@app.route("/new", methods=["POST"])
def new():
    data = {
        "helloworld": request.form["helloworld"]
    }

    db.appdb.insert_one(data)

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

