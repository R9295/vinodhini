var db = new PouchDB('offline_notes')
//
function store_note(when_posted,image,text,note,status,title,id){
	db.put({
		_id: id,
		image: image,
		text: text,
		note: note,
		status: status,
		note: note,
		when_posted: when_posted
	}).then(function(response){
		console.log(response)
		db.get(id).then(function(doc){
			console.log(doc)
		}).catch(function(err){
			console.log(err)
		})
		
	}).catch(function(err){
		console.log(err)
	})

}