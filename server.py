from flask import Flask,render_template,redirect,request,make_response,redirect,url_for,jsonify
from pymongo import MongoClient
from argon2 import PasswordHasher
import json
#to query collections by their Id
from bson.objectid import ObjectId
from time import gmtime, strftime
import string 
import random
from time import gmtime,strftime
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



#Home
@app.route('/',methods=['GET','POST'])
def home():
	db.active.delete_many({})
	if db.code.find().count() == 0:
		return redirect('/code')
	if request.method == 'POST':
		response = {}
		password = db.code.find_one()
		try: 
			ph.verify(password['code'],request.json['code'])
			active_user = {
			'code': key_gen()
			}
			response['response'] = 'success'
			response['code'] = active_user['code']
			db.active.insert_one(active_user)

			response = json.dumps(response)
			return response 
		except:
			response['response'] = 'failure'
			response = json.dumps(response)
			return response 

	return render_template('home.html')



@app.route('/code',methods=['GET','POST'])
def add_code():
	if request.method == 'POST':
		data = {
		'code':ph.hash(request.form['code'])
		}
		 
		db.code.insert_one(data)
		return redirect('/')
	return render_template('code.html')


#Add Note
@app.route('/add_note', methods=['GET','POST'])
def add_note():
	status = request.cookies.get('logged')
	status = db.active.find({'code':status}).count()
	if status == 0:
		return redirect('/')
	if request.method == 'POST':
		
		data = {
		'note' : request.json['note'],
		'title': request.json['title'],
		'status':'incomplete',
		'when_uploaded':strftime("%a, %d %b %Y", gmtime()),
		'text': request.json['text'],
		'img': request.json['img'],
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
	status = request.cookies.get('logged')
	status = db.active.find({'code':status}).count()
	if status == 0:
		return redirect('/')
	notes = db.notes.find({'status' : 'incomplete'})
	return render_template('view_notes.html',notes=notes)

#View Notes
@app.route('/view_notes/finished', methods=['GET'])
def view_notes_finished():
	status = request.cookies.get('logged')
	status = db.active.find({'code':status}).count()
	if status == 0:
		return redirect('/')
	notes = db.notes.find({'status' : 'complete'})
	return render_template('view_finished_notes.html',notes=notes)


#View Individual Note
@app.route('/note/<id>', methods=['GET','POST'])
def view_inidividual_note(id):
	status = request.cookies.get('logged')
	status = db.active.find({'code':status}).count()
	if status == 0:
		return redirect('/')
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

@app.route('/logout')
def logout():
	key = request.cookies.get('key')
	error = None
	if db.active.find().count() != 0:
		db.active.delete_many({})
		resp = make_response(redirect('/'))
    	resp.set_cookie('logged','',expires=0)
    	return resp

    	





if __name__ == "__main__":
	app.run()