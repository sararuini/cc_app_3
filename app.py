from flask import Flask, render_template, jsonify, request
import json
import os
import requests
from flask_sqlalchemy import SQLAlchemy
import urllib.request

#app setup
#sources consulted
# https://stackoverflow.com/questions/36636703/trying-to-run-the-sql-alchemy-tutorial-steps-cant-import-db-from-console-impo
# https://stackoverflow.com/questions/448271/what-is-init-py-for
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cat_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#database setup
db = SQLAlchemy(app)

#url templates
url_template = "https://api.thecatapi.com/v1"
#json cat breed data

#DATABASE MODELLING
#creating a model to insert cat breeds into database
#source consulted: https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/
class CatBreed(db.Model):
    __tablename__ = 'cat_breeds'
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(50))
    temperament = db.Column(db.String(100))
    origin = db.Column(db.String(50))
    description = db.Column(db.String(200))
    life_span = db.Column(db.String(50))

    #defining how CatBreed objs are going to be printed
    def _repr__(self):
        return '<CatBreed {}>'.format(self.name, self.temperament, self.origin, self.life_span)
#authentication key passed in headers 
headers = {'x-api-key': '17816ca0-ede7-4033-a4cf-2dcf0b30a1f1'}

#populating cat breed database
def populating_breeds_db():
    request = urllib.request.urlopen("https://api.thecatapi.com/v1/breeds?api_key=17816ca0-ede7-4033-a4cf-2dcf0b30a1f1")
    content = request.read()
    encoding = request.info().get_content_charset('utf-8')
    cat_breeds =  json.loads(content.decode(encoding))
    breeds_to_add = []
    for breed in cat_breeds:
        breed_id = breed['id']
        breed_name = breed['name']
        breed_temperament = breed['temperament']
        breed_origin = breed['origin']
        breed_description = breed['description']
        breed_life_span = breed['life_span']
        #instantiating new breed instance
        new_breed_entry = CatBreed(id=breed_id, name=breed_name, temperament=breed_temperament, origin=breed_origin, description= breed_description, life_span =breed_life_span)
        breeds_to_add.append(new_breed_entry)
    #adding all instances to datbaase
    db.session.add_all(breeds_to_add)
    db.session.commit()

#ROUTES!!!!

#GET REQUESTS

#get request to homepage
@app.route("/", methods=['GET'])
def homepage():
    return render_template("homepage.html"), 201

#get request with breeds
#source consulted to write this get request: https://github.com/PrettyPrinted/weather_app_flask/blob/master/app.py
@app.route("/breeds", methods=['GET'])
def all_breeds():
    breeds = CatBreed.query.all()
    all_breeds = []
    for breed in breeds:
        cat_breed = {
            'id' : breed.id,
            'name' : breed.name,
            'temperament' : breed.temperament,
            'origin' : breed.origin,
            'description' : breed.description
        }
        all_breeds.append(cat_breed) 
        #source used for jsonifying data https://stackoverflow.com/questions/34392892/how-to-convert-sqlalchemy-query-result-to-json-data
        jsonified_breeds = json.dumps(all_breeds)
        string_breeds = json.loads(jsonified_breeds)
        return jsonify(all_breeds), 201

# #get request to retrieve a specific cat breed based on breed id
# @app.route('/breeds/<id>', methods=['GET', 'PUT', 'DELETE'])
# def retrieve_breed(id):
#         if
#         #if cat breed found print status code 200
#         #if cat breed not found print status code 404
#         print("the cat returns")

# #POST      
# #post request to database to post your own cat picture
# @app.route('/breeds/', methods=['POST'])
# def retrieve_breed(id):
#         #if category breed found print status code 200
#         #if category not found print status code 404
#         print("the cat returns")

#run app
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
