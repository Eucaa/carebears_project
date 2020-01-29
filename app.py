import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.utils import secure_filename

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
    listOfCharacterFromDb = list(mongo.db.carebears_collection.find())
    count = 0
    for character in listOfCharacterFromDb:
        category_name = mongo.db.categories.find_one( { "_id": character['category_id'] } )['category_name']
        voice_actor_name = mongo.db.voice_actor.find_one( { "_id": character['voice_actor_id'] } )['voice_actor']

        listOfCharacterFromDb[count]['category_name'] = category_name
        listOfCharacterFromDb[count]['voice_actor_name'] = voice_actor_name
        count = count + 1

    return render_template("character_list.html", characters=listOfCharacterFromDb)


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
    print("Updated")
    return render_template("add_bear.html", characters=mongo.db.carebears_collection.find(), categories=mongo.db.categories.find())


@app.route('/carebear_info/<character_id>')
def character_info(character_id):
    characterFromDb = mongo.db.carebears_collection.find_one({'_id': ObjectId(character_id)})
    print(characterFromDb)
    category_name = mongo.db.categories.find_one( { "_id": characterFromDb['category_id'] } )['category_name']
    voice_actor_name = mongo.db.voice_actor.find_one( { "_id": characterFromDb['voice_actor_id'] } )['voice_actor']

    characterFromDb['category_name'] = category_name
    characterFromDb['voice_actor_name'] = voice_actor_name

    return render_template("carebear_info.html", character=characterFromDb)


def upload_image(files):
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

    fileName = secure_filename(image.filename)
    directory = os.path.join(os.getcwd(), app.config["IMAGE_UPLOAD"][1:])

    # check if upload directory exists else create it
    if not os.path.exists(directory):
        os.makedirs(directory)

    filePath = os.path.join(directory, fileName)    
    image.save(filePath)
    return os.path.join(app.config["IMAGE_UPLOAD"], fileName) 


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


@app.route('/character-search')
def search():
    search = request.args.get('search')
    results = list(mongo.db.carebears_collection.aggregate([
        {
            "$match": {
                "$text": {
                    "$search": search
                }
            }
        },
        {
            "$lookup": {
                "from": "categories",
                "localField": "category_id",
                "foreignField": "_id",
                "as": "categories"
            }
        },
        {
            "$unwind": "$categories"
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
            "$unwind": "$voiceactors"
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
    ]))

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

    if character['image_path'] is None:
        # upload an image from form
        path = upload_image(request.files)
        formValues['image_path'] = None
        if path is not None:
            formValues['image_path'] = path
    else:
        formValues['image_path'] = character['image_path']

    voice_actor_db = mongo.db.voice_actor.find_one({'voice_actor': formValues['voice_actor_name']})
    if(voice_actor_db is None):
        # aanmaken
        mongo.db.voice_actor.insert_one({'voice_actor': formValues['voice_actor_name']})
        voice_actor_db = mongo.db.voice_actor.find_one({'voice_actor': formValues['voice_actor_name']})
    
    formValues['voice_actor_id'] = voice_actor_db['_id']
    formValues['category_id'] = ObjectId(formValues['category_id'])

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
        'image_path': formValues['image_path']
    })

    return redirect(url_for('character_info', character_id=character['_id']))
    #end add


@app.route('/insert_character', methods=['POST'])
def insert_character():
    formValues = request.form.to_dict()

    # upload an image from form
    path = upload_image(request.files)
    if path is not None:
        formValues['image_path'] = path

    voice_actor_db = mongo.db.voice_actor.find_one({'voice_actor': formValues['voice_actor_name']})
    if(voice_actor_db is None):
        # aanmaken
        mongo.db.voice_actor.insert_one({'voice_actor': formValues['voice_actor_name']})
        voice_actor_db = mongo.db.voice_actor.find_one({'voice_actor': formValues['voice_actor_name']})

    formValues['voice_actor_id'] = voice_actor_db['_id']
    formValues['category_id'] = ObjectId(formValues['category_id'])

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
