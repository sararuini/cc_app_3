
from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import json
import requests
import urllib.request
import app

#populating database
def populate_breeds_db():
    with app.app_context():
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
            new_breed_entry = app.CatBreed(id=breed_id, name=breed_name, temperament=breed_temperament, origin=breed_origin, description= breed_description, life_span =breed_life_span)
            app.db.session.add(new_breed_entry)
        app.db.session.commit()