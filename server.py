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
	tags = db.tags.find()
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
		'tag':request.json['tag']
		}
		db.notes.insert_one(data)		
		response = {}
		response['response'] = 'success'
		response = json.dumps(response)
		return response
		

	return render_template('add_note.html',tags=tags)

@app.route('/get_individual', methods=['GET','POST'])
def get_individual():
	status = request.cookies.get('logged')
	status = db.active.find({'code':status}).count()
	if status == 0:
		return redirect('/')
	if request.method == 'POST':
		note = db.notes.find({'_id':ObjectId(request.json['id'])}).count()
		print note
		if note == 0:
			response = {}
			response['response'] = 'failure'
			response = json.dumps(response)
			return response
		if note == 1:
			note = db.notes.find_one({'_id':ObjectId(request.json['id'])})
			response = {}
			response['response'] = 'success'
			response['note'] = note['note']
			response['title'] = note['title']
			response['status'] = note['status']
			response['when_uploaded'] = note['when_uploaded']
			response['text'] = note['text']
			response['img'] = note['img']
			response['tag'] = note['tag']
			response = json.dumps(response)
			return response


#View Notes
@app.route('/view_notes', methods=['GET','POST'])
def view_notes():
	filtered_notes = []
	status = request.cookies.get('logged')
	status = db.active.find({'code':status}).count()
	if status == 0:
		return redirect('/')
	notes = db.notes.find({'status' : 'incomplete'})
	tags = db.tags.find()
	if request.method == 'POST':

		if request.json['tag'] == 'All':
			notes = db.notes.find({'status':'incomplete'})
			for i in notes:
				filtered_notes.append([i['note'],i['title'],str(i['_id'])])
			response = {}
			response['response'] = 'success'
			response['notes'] = filtered_notes
			response = json.dumps(response)
			return response
			


		tag = request.json['tag']
		notes = db.notes.find({'tag':tag,'status':'incomplete'})
		for i in notes:
			filtered_notes.append([i['note'],i['title'],str(i['_id'])])
		response = {}
		response['response'] = 'success'
		response['notes'] = filtered_notes
		response = json.dumps(response)
		return response

	return render_template('view_notes.html',notes=notes,tags=tags)

#View Notes
@app.route('/view_notes/finished', methods=['GET','POST'])
def view_notes_finished():
	filtered_notes = []
	status = request.cookies.get('logged')
	status = db.active.find({'code':status}).count()
	if status == 0:
		return redirect('/')
	notes = db.notes.find({'status' : 'complete'})
	tags = db.tags.find()
	if request.method == 'POST':

		if request.json['tag'] == 'All':
			notes = db.notes.find({'status':'complete'})
			for i in notes:
				filtered_notes.append([i['note'],i['title'],str(i['_id'])])
			response = {}
			response['response'] = 'success'
			response['notes'] = filtered_notes
			response = json.dumps(response)
			return response
			


		tag = request.json['tag']
		notes = db.notes.find({'tag':tag,'status':'complete'})
		for i in notes:
			filtered_notes.append([i['note'],i['title'],str(i['_id'])])
		response = {}
		response['response'] = 'success'
		response['notes'] = filtered_notes
		response = json.dumps(response)
		return response
	return render_template('view_finished_notes.html',notes=notes,tags=tags)



@app.route('/delete_this', methods=['POST'])
def delete_this():
	id = request.json['id']
	note = db.notes.find({'_id':ObjectId(id)}).count()
	if note != 1:
		response = {}
		response['response'] = 'failure'
		response = json.dumps(response)
		return response
	if note == 1:
		db.notes.delete_one({'_id':ObjectId(id)})
		response = {}
		response['response'] = 'success'
		response = json.dumps(response)
		return response



@app.route('/finish_note', methods=['POST'])
def finish_one():
	note = db.notes.find_one({'_id':ObjectId(request.json['id'])})
	note['status'] = 'complete'
	db.notes.save(note)
	response = {}
	response['response'] = 'success'
	response = json.dumps(response)
	return response

#Remove Note
@app.route('/delete_note/<id>', methods=['GET','POST'])
def delete_note(id):
	note = db.notes.find_one({'_id':ObjectId(request.json['id'])})
	print note
	note['status'] = 'complete'
	db.notes.save(note)
	response = {}
	response['response'] = 'success'
	response = json.dumps(response)
	return response


@app.route('/create_tag', methods=['POST'])
def create_tag():
	tag = request.json['tag']
	data = {
	'tag':tag
	}
	db.tags.insert_one(data)
	response = {}
	response['response'] = 'success'
	response = json.dumps(response)
	return response

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
	app.run(debug=True,host='0.0.0.0')