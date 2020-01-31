import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import base64

app = Flask(__name__)
app.config['IMAGE_UPLOAD'] = '/static/upload'
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG"]
app.config['MAX_IMAGE_SIZE'] = 3 * 1024 * 1024  # max mb = 3mb

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
    results = list(mongo.db.carebears_collection.aggregate(createSearchQuery(None)))
    return render_template("character_list.html", characters=results)


@app.route('/get_carebears_collection')
def carebears_collection():
    return render_template("carebears_collection.html", collection=mongo.db.carebears_collection.find())


@app.route('/sign_up')
def signUp():
    return render_template("sign_up.html")


@app.route('/sign_in')
def signIn():
    return render_template("sign_in.html")


@app.route('/character_creation')
def addBear():
    return render_template("add_bear.html", characters=mongo.db.carebears_collection.find(), categories=mongo.db.categories.find())


@app.route('/carebear_info/<character_id>')
def character_info(character_id):
    characterFromDb = mongo.db.carebears_collection.find_one({'_id': ObjectId(character_id)})
    if characterFromDb['category_id'] is not None:
        category_name = mongo.db.categories.find_one( { "_id": characterFromDb['category_id'] } )['category_name']        
        characterFromDb['category_name'] = category_name

    if characterFromDb['voice_actor_id'] is not None:
        voice_actor_name = mongo.db.voice_actor.find_one( { "_id": characterFromDb['voice_actor_id'] } )['voice_actor']
        characterFromDb['voice_actor_name'] = voice_actor_name

    image = None
    if characterFromDb['image_blob'] is not None:
        image = characterFromDb['image_blob'].decode()

    return render_template("carebear_info.html", character=characterFromDb, image=image)


def encode_image(files):
    if files is None:
        return None

    if len(files) == 0:
        return None

    # create handle for the image.
    image = files['image']

    # seek till end of file
    image.seek(0, os.SEEK_END)

    # determine file length in bytes
    file_length = image.tell()

    # reset stream position back to 0 so we can later process the complete file.
    image.seek(0)

    if not allowed_image_filesize(file_length):
        print("Filesize exceeded maximum limit")
        return None

    if image.filename == "":
        print("No filename")
        return None

    if not allowed_image(image.filename):
        print("File not allowed")
        return None
    encoded = base64.b64encode(image.read())
    return encoded


def allowed_image(filename):

    # Only files with a . in the filename
    if "." not in filename:
        return False

    # Split the extension from the filename
    ext = filename.rsplit(".", 1)[1]

    # Check if extension is in ALLOWED_IMAGE_EXTENSIONS
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


def allowed_image_filesize(filesize):
    if int(filesize) <= app.config["MAX_IMAGE_SIZE"]:
        return True
    else:
        return False


def createSearchQuery(search):
    searchQuery = [
        {
            "$lookup": {
                "from": "categories",
                "localField": "category_id",
                "foreignField": "_id",
                "as": "categories"
            }
        },
        {
            "$unwind": {
                "path": "$categories",
                "preserveNullAndEmptyArrays": True
            }
        },
        {
            "$lookup": {
                "from": "voice_actor",
                "localField": "voice_actor_id",
                "foreignField": "_id",
                "as": "voiceactors"
            }
        },
        {
            "$unwind": {
                "path": "$voiceactors",
                "preserveNullAndEmptyArrays": True
            }
        },
        {
            "$sort": {
                "character_name": 1
            }
        },
        {
            "$project": {
                "_id": 1,
                "character_name": 1,
                "color": 1,
                "belly_badge": 1,
                "gender": 1,
                "residence": 1,
                "release_date": 1,
                "story": 1,
                "category_name": "$categories.category_name",
                "voice_actor_name": "$voiceactors.voice_actor"
            }
        }
    ]
    if search is not None:
        matchQuery = {
            "$match": {
                "$text": {
                    "$search": search
                }
            }
        }
        searchQuery.insert(0, matchQuery)
        return searchQuery
    else:
        return searchQuery

@app.route('/character-search')
def search():
    searchQuery = createSearchQuery(request.args.get('search'))
    results = list(mongo.db.carebears_collection.aggregate(searchQuery))
    print(results)

    return render_template("character_list.html", characters=results)

@app.route('/edit_character/<character_id>')
def edit_character(character_id):
    the_character = mongo.db.carebears_collection.find_one({'_id': ObjectId(character_id)})
    all_categories = mongo.db.categories.find()
    the_voice_actor = mongo.db.voice_actor.find_one({'_id': the_character['voice_actor_id']})
    return render_template("edit_character.html", carebears=the_character, categories=all_categories, voice_actor=the_voice_actor)


@app.route('/update_character/<character_id>', methods=['POST'])
def update_character(character_id):
    formValues = request.form.to_dict()

    character = mongo.db.carebears_collection.find_one({'_id': ObjectId(character_id)}) #looking for one bear only

    if character['image_blob'] is None:
        # upload an image from form
        imgAsBase64 = encode_image(request.files)
        if imgAsBase64 is not None:
            formValues['image_blob'] = imgAsBase64
        else:
            formValues['image_blob'] = None
    else:
        formValues['image_blob'] = character['image_blob']

    if formValues['voice_actor_name'] != "":
        voice_actor_db = mongo.db.voice_actor.find_one({'voice_actor': formValues['voice_actor_name']})
        if(voice_actor_db is None):
            # aanmaken
            mongo.db.voice_actor.insert_one({'voice_actor': formValues['voice_actor_name']})
            voice_actor_db = mongo.db.voice_actor.find_one({'voice_actor': formValues['voice_actor_name']})
        formValues['voice_actor_id'] = voice_actor_db['_id']        
    else:
        formValues['voice_actor_id'] = None

    if formValues['category_id'] == 'Invalid':
        formValues['category_id'] = None
    else:
        formValues['category_id'] = ObjectId(formValues['category_id'])

    if formValues['gender'] == 'Invalid':
        formValues['gender'] = None

    if formValues['residence'] == 'Invalid':
        formValues['residence'] = None


    mongo.db.carebears_collection.update({'_id': ObjectId(character_id)},
    {
        'character_name': formValues['character_name'],
        'category_id': formValues['category_id'],
        'color': formValues['color'],
        'belly_badge': formValues['belly_badge'],
        'gender': formValues['gender'],
        'residence': formValues['residence'],
        'release_date': formValues['release_date'],
        'voice_actor_id': formValues['voice_actor_id'],
        'story': formValues['story'],
        'image_blob': formValues['image_blob']
    })

    return redirect(url_for('character_info', character_id=character['_id']))
    #end add


@app.route('/insert_character', methods=['POST'])
def insert_character():
    formValues = request.form.to_dict()

    # upload an image from form
    imgAsBase64 = encode_image(request.files)
    if imgAsBase64 is not None:
        formValues['image_blob'] = imgAsBase64
    else:
        formValues['image_blob'] = None

    if formValues['voice_actor_name'] != "":
        voice_actor_db = mongo.db.voice_actor.find_one({'voice_actor': formValues['voice_actor_name']})
        if(voice_actor_db is None):
            # aanmaken
            mongo.db.voice_actor.insert_one({'voice_actor': formValues['voice_actor_name']})
            voice_actor_db = mongo.db.voice_actor.find_one({'voice_actor': formValues['voice_actor_name']})

        formValues['voice_actor_id'] = voice_actor_db['_id']
    else:
        formValues['voice_actor_id'] = None

    if formValues['category_id'] == 'Invalid':
        formValues['category_id'] = None
    else:
        formValues['category_id'] = ObjectId(formValues['category_id'])

    if formValues['gender'] == 'Invalid':
        formValues['gender'] = None

    if formValues['residence'] == 'Invalid':
        formValues['residence'] = None

    formValues.pop('voice_actor_name', None)
    formValues.pop('image', None)

    mongo.db.carebears_collection.insert_one(formValues)
    return redirect(url_for('character_list'))


@app.route('/delete_character/<character_id>')
def delete_character(character_id):
    mongo.db.carebears_collection.remove({'_id': ObjectId(character_id)})
    return redirect(url_for('character_list'))


if __name__ == '__main__':
    print(os.environ.get('IP'))
    app.run(host=os.environ.get('IP', '0.0.0.0'),
            port=int(os.environ.get('PORT', '8080')),
            debug=True)
