import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'carebears_db'
app.config["MONGO_URI"] = os.environ.get('MONGODB_CONNECTIONSTRING', 'mongodb://localhost') +  "/" + app.config["MONGO_DBNAME"] + "?retryWrites=true&w=majority"

mongo = PyMongo(app)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/about')
def about():
    return render_template("about.html")    


@app.route('/get_carebears_collection')
def get_carebears_collection():
    return render_template("carebears_collection.html", collections=mongo.db.carebears_collection.find())

if __name__ == '__main__':
    print(os.environ.get('IP'))
    app.run(host=os.environ.get('IP', '0.0.0.0'),
            port=int(os.environ.get('PORT', '8080')),
            debug=True)
