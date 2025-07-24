var ws = new WebSocket('ws://127.0.0.1:8000/ws/wsc/')
ws.onopen =  function(){
    console.log('Websocket Connection open...')
    ws.send("hi,message from client")
}
ws.onmessage = function(event){
    console.log("message recieved from server..",event)
    console.log(event.data)
    document.getElementById("ct").innerText= event.data
}