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
import base64

# id_generator
def key_gen(size=10, chars=string.ascii_uppercase + string.digits):
  return ''.join(random.choice(chars) for _ in range(size))


ph = PasswordHasher()

#Connecting to DB
client = MongoClient()
db = client.notes



app = Flask(__name__)


#Configuring where photos should be uploaded.
photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'


#Home
app.route('/')
def home():
	return render_template('home.html')


#Add Note
@app.route('/add_note', methods=['GET','POST'])
def add_note():

	if request.method == 'POST':
		data = {
		'img' : request.json['img'],
		'title': request.json['title'],
		'status':'incomplete',
		'when_uploaded':strftime("%a, %d %b %Y", gmtime())
		}
		db.notes.insert_one(data)
		
		note = db.notes.find_one({'title':data['title']})
		url = '%s'%(note['_id'])
		response = {}
		response['response'] = 'success'
		response['url'] = url
		response = json.dumps(response)
		return response
		

	return render_template('add_note.html')



#View Notes
@app.route('/view_notes', methods=['GET'])
def view_notes():
	notes = db.notes.find()
	return render_template('view_notes.html',notes=notes)


#View Individual Note
@app.route('/note/<id>', methods=['GET','POST'])
def view_inidividual_note(id):
	note = db.notes.find_one({'_id':ObjectId(id)})
	if request.method == 'POST':
		note['status'] = 'complete'
		db.notes.save(note)
		response = {}
		response['response'] = 'success'
		response = json.dumps(response)
		return response
	return render_template('individual_note.html', note=note)

#Search
@app.route('/search', methods=['GET','POST'])
def search():
	pass


#Remove Note
@app.route('/delete_note/<id>', methods=['GET','POST'])
def delete_note(id):
	pass



#Email Notifications




if __name__ == "__main__":	
	app.run(host='0.0.0.0')