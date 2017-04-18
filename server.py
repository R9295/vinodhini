from flask import Flask,render_template,redirect,request,make_response,redirect,url_for,jsonify
from pymongo import MongoClient
from argon2 import PasswordHasher
import json
from bcrypt import hashpw,gensalt
#to query collections by their Id
from bson.objectid import ObjectId
from time import gmtime, strftime
import string 
import random
from time import gmtime,strftime
from flask_uploads import UploadSet, configure_uploads, IMAGES
from datetime import *
import datetime

# id_generator
def key_gen(size=10, chars=string.ascii_uppercase + string.digits):
  return ''.join(random.choice(chars) for _ in range(size))


ph = PasswordHasher()

#Connecting to DB
client = MongoClient()
db = client.notes




app = Flask(__name__)

@app.route("/")
def home():
    return "Hello XD"

if __name__ == "__main__":
    app.run(debug=True)