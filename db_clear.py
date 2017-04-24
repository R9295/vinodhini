from pymongo import *
client = MongoClient()
db = client.notes

db.notes.delete_many({})
print 'Deleted all notes'

db.code.delete_many({})
print 'Deleted all codes'
