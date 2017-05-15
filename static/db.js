//function init(){
//new PouchDB('offline_notes').destroy().then(function () {
 // console.log('clear')

//}).catch(function (err) {
 // console.log(err)
//})
//}

 var db = new PouchDB('offline_notes')
function store_note(when_posted,image,text,note,status,title,id){
  db.get(id).then(function (doc){
    console.log('exists')
  }).catch(function (err){
    db.put({
    _id: id,
    image: image,
    text: text,
    note: note,
    status: status,
    note: note,
    when_posted: when_posted
  }).then(function(response){
    console.log('done')
  }).catch(function(err){
    console.log(err)
  })
  })



}

    function asd(){
      db.allDocs({
  include_docs: true,
  attachments: true
}).then(function (result) {
  console.log(result.rows)
}).catch(function (err) {
  console.log(err);
});
  
}