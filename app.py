from flask import Flask, render_template, jsonify, request
import json
import requests
from flask_sqlalchemy import SQLAlchemy

#app + db creation and setup
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cat_breeds.db'

#authentication key passed in headers 
headers = {'x-api-key': '17816ca0-ede7-4033-a4cf-2dcf0b30a1f1'}

#url templates
url_template = "https://api.thecatapi.com/v1"
#resource used for caching setup: https://pypi.org/project/Flask-SQLAlchemy-Caching/
#database setup
db = SQLAlchemy()

#DATABASE MODELLING
#creating a model to insert cat breeds into database
#source consulted: https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/
class CatBreed(db.Model):
    __tablename__ = 'cat_breed'
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(50))
    temperament = db.Column(db.String(100))
    origin = db.Column(db.String(50))
    description = db.Column(db.String(200))
    wikipedia_url = db.Column(db.String(200))

@app.route("/database", methods='GET')
def homepage():
    return render_template("homepage.html")

#app + db creation and setup
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cat_breeds.db'

#run app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
