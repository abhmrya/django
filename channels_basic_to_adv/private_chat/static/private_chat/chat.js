const messagesDiv = document.getElementById("messages");

const input = document.getElementById("message");

const sendBtn = document.getElementById("sendBtn");

const typingDiv = document.getElementById("typing");

const statusDiv = document.getElementById("status");


// =====================================
// Auto Scroll
// =====================================

function scrollBottom(){

    messagesDiv.scrollTop = messagesDiv.scrollHeight;

}


// =====================================
// Add Message
// =====================================

function addMessage(sender,message,time){

    const div=document.createElement("div");

    if(sender===currentUser){

        div.className="message me";

    }else{

        div.className="message other";

    }

    div.innerHTML=`

        <div class="sender">

            ${sender}

        </div>

        <div>

            ${message}

        </div>

        <div class="time">

            ${time}

        </div>

    `;

    messagesDiv.appendChild(div);

    scrollBottom();
2
}


// =====================================
// Send Message
// =====================================

sendBtn.onclick=function(){

    const message=input.value.trim();

    if(message==="") return;

    socket.send(

        JSON.stringify({

            action:"message",

            message:message

        })

    );

    input.value="";

};


// =====================================
// Enter Key
// =====================================

input.addEventListener(

    "keypress",

    function(e){

        if(e.key==="Enter"){

            sendBtn.click();

        }

    }

);


// =====================================
// Typing
// =====================================

let typingTimer;

input.addEventListener(

    "input",

    function(){

        socket.send(

            JSON.stringify({

                action:"typing"

            })

        );

        clearTimeout(typingTimer);

        typingTimer=setTimeout(

            ()=>{

                socket.send(

                    JSON.stringify({

                        action:"stop_typing"

                    })

                );

            },

            1000

        );

    }

);


// =====================================
// Socket Open
// =====================================

socket.onopen=function(){

    console.log("Connected");

};


// =====================================
// Receive Data
// =====================================

socket.onmessage=function(e){

    const data=JSON.parse(e.data);


    // ===========================
    // History
    // ===========================

    if(data.type==="history"){

        messagesDiv.innerHTML="";

        data.messages.forEach(

            function(msg){

                addMessage(

                    msg.sender,

                    msg.message,

                    msg.time

                );

            }

        );

    }


    // ===========================
    // New Message
    // ===========================

    else if(data.type==="message"){

        addMessage(

            data.sender,

            data.message,

            data.time

        );

    }


    // ===========================
    // Typing
    // ===========================

    else if(data.type==="typing"){

        typingDiv.innerHTML=

            data.user+" is typing...";

    }


    // ===========================
    // Stop Typing
    // ===========================

    else if(data.type==="stop_typing"){

        typingDiv.innerHTML="";

    }


    // ===========================
    // Online
    // ===========================

    else if(data.type==="online_status"){

        if(data.online){

            statusDiv.innerHTML="🟢 Online";

        }else{

            statusDiv.innerHTML="⚫ Offline";

        }

    }


    // ===========================
    // Read Receipt
    // ===========================

    else if(data.type==="read_receipt"){

        console.log(

            "Read :",

            data.message_id

        );

    }

};


// =====================================
// Socket Close
// =====================================

socket.onclose=function(){

    console.log("Disconnected");

};