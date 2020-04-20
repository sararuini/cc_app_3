from flask import Flask, render_template, jsonify, request
import json
import os
import requests
from flask_sqlalchemy import SQLAlchemy
import urllib.request

#app + db creation and setup
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cat_breeds.db'
app.app_context().push()

#authentication key passed in headers 
headers = {'x-api-key': '17816ca0-ede7-4033-a4cf-2dcf0b30a1f1'}

#url templates
url_template = "https://api.thecatapi.com/v1"
#database setup
db = SQLAlchemy(app)

#DATABASE MODELLING
#creating a model to insert cat breeds into database
#source consulted: https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/
class CatBreed(db.Model):
    __tablename__ = 'cat_breed'
    id = db.Column(db.String(50), primary_key=True, unique=True)
    name = db.Column(db.String(50), unique=True)
    temperament = db.Column(db.String(100), unique=False)
    origin = db.Column(db.String(50), unique=False)
    description = db.Column(db.String(200), unique=False)
    life_span = db.Column(db.String(50), unique=False)

    #defining how CatBreed objs are going to be printed
    def _repr__(self):
        return '<CatBreed {}>'.format(self.name, self.temperament, self.orign, self.life_span)

#populating database
def populate_breeds_db():
    #with open('breeds.json', encoding='utf-8') as cat_breeds:
    request = urllib.request.urlopen(
    "https://api.thecatapi.com/v1/breeds?api_key=17816ca0-ede7-4033-a4cf-2dcf0b30a1f1")
    content = request.read()
    encoding = request.info().get_content_charset('utf-8')
    cat_breeds =  json.loads(content.decode(encoding))
        #all_breeds = json.load(cat_breeds)
    for breed in cat_breeds:
        breed_id = breed['id']
        breed_name = breed['name']
        breed_temperament = breed['temperament']
        breed_origin = breed['origin']
        breed_description = breed['description']
        breed_life_span = breed['life_span']
        new_breed_entry = CatBreed(id=breed_id, name=breed_name, temperament=breed_temperament, origin=breed_origin, description= breed_description, life_span =breed_life_span)
        db.session.add(new_breed_entry)
    db.session.commit()

populate_breeds_db()

@app.route("/", methods=['GET'])
def homepage():
    return render_template("homepage.html")

#run app
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
