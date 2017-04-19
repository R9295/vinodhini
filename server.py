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
		due_date = request.form['start_date']
		due_year = start_date[0:4]
		due_month = start_date[5:7]
		due_day = start_date[8:10]
		due_date= start_day+'/'+start_month+'/'+start_year

		data = {
		'title': request.form['title'],
		'note': request.form['note'],
		'due': request.form['due'],
		'status':'incomplete',
		'when_uploaded':strftime("%a, %d %b %Y", gmtime())
		}
	return render_template('add_note.html')



#View Notes
@app.route('/view_notes', methods=['GET'])
def view_notes():
	return render_template('view_notes.html')


#View Individual Note
@app.route('/note/<id>', methods=['GET','POST'])
def view_inidividual_note(id):
	return render_template('individual_note.html')

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
	configure_uploads(app, photos)	
	app.run(debug=True)