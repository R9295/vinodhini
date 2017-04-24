//Service-Worker-Allowed: "/" 

self.addEventListener( "fetch" , function (event) {
    //fetch request as specified by event object 
    console.log(event.request); //Note that Request and Response are also objects 
});