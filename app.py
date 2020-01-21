import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'carebears_db'
app.config["MONGO_URI"] = os.environ.get('MONGODB_CONNECTIONSTRING', 'mongodb://localhost') + "/" + app.config["MONGO_DBNAME"] + "?retryWrites=true&w=majority"

mongo = PyMongo(app)


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/character_list')
def character_list():
    listOfCharacterFromDb = list(mongo.db.carebears_collection.find())
    count = 0
    for character in listOfCharacterFromDb:
        category_name = mongo.db.categories.find_one( { "_id": character['category_id'] } )['category_name']
        voice_actor_name = mongo.db.voice_actor.find_one( { "_id": character['voice_actor_id'] } )['voice_actor']

        listOfCharacterFromDb[count]['category_name'] = category_name
        listOfCharacterFromDb[count]['voice_actor_name'] = voice_actor_name
        count = count + 1

    return render_template("character_list.html", characters = listOfCharacterFromDb)


@app.route('/get_carebears_collection')
def carebears_collection():
    return render_template("carebears_collection.html")


@app.route('/sign_up')
def signUp():
    return render_template("sign_up.html")


@app.route('/sign_in')
def signIn():
    return render_template("sign_in.html")


@app.route('/character_creation')
def addBear():
    print("Updated")
    return render_template("add_bear.html", characters=mongo.db.carebears_collection.find(), categories=mongo.db.categories.find())


@app.route('/character_info')
def character_info():
    return render_template("carebear_info.html")  #Later, add a , and delete )
    category = mongo.db.carebears_collection.find_one({'_id': ObjectId(carebears_collection_id)})


@app.route('/edit_character/<carebears_collection_id>')
def edit_character(carebears_collection_id):
    the_character = mongo.db.carebears_collection.find_one({'_id': ObjectId(carebears_collection_id)})
    all_categories = mongo.db.categories.find()
    return render_template("edit_character.html", carebears=the_character, categories=all_categories)


@app.route('/update_character/<carebears_collection_id>', methods=['POST'])
def update_character(carebears_collection_id):
    characters = mongo.db.character_collection
    characters.update({'_id': ObjectId(carebears_collection_id)},
    {
        'character_name': request.form.get('character_name'),
        'category_name': request.form.get('catergory_name'),
        'color': request.form.get('color'),
        'belly_badge': request.form.get('belly_badge'),
        'gender': request.form.get('gender'),
        'residence': request.form.get('residence'),
        'release_date': request.form.get('release_date'),
        'voice_actor': request.form.get('voice_actor')
    })
    return redirect(url_for('get_carebears_collection'))


@app.route('/insert_character', methods=['POST'])
def insert_character():
    characters = mongo.db.carebears_collection  # Get the tasks collection from Mongo.
    characters.insert_one(request.form.to_dict())
    return redirect(url_for('get_carebears_collection'))


@app.route('/delete_character/<carebears_collection_id>')
def delete_character(carebears_collection_id):
    mongo.db.carebears_collection_id.remove({'_id': ObjectId(carebears_collection_id)})
    return redirect(url_for('get_carebears_collection'))

"""
round line 11 in add_bear view: <!--<form action="{{ url_for('insert_character') }}" method="POST"  class="col s12">-->
"""  

if __name__ == '__main__':
    print(os.environ.get('IP'))
    app.run(host=os.environ.get('IP', '0.0.0.0'),
            port=int(os.environ.get('PORT', '8080')),
            debug=True)
