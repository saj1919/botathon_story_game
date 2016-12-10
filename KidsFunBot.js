function MessageHandler(context, event) {
    my_msg = encodeURI(event.message);
    
    context.console.log("MY MSG : "+my_msg);
    my_url = "http://swapnil.hellohaptik.com:8080/main_api";
    my_param = "my_text="+my_msg;
    context.console.log("MY URL : "+my_url+" , MY PARAM : "+my_param)
    context.simplehttp.makeGet(my_url+"?"+my_param);
    return;
}

/** Functions declared below are required **/
function EventHandler(context, event) {
    if(! context.simpledb.botleveldata.numinstance)
        context.simpledb.botleveldata.numinstance = 0;
    numinstances = parseInt(context.simpledb.botleveldata.numinstance) + 1;
    context.simpledb.botleveldata.numinstance = numinstances;
    context.sendResponse("Type 'poem' to play poem Creation game. Type 'yoda' to get yodish echo. Type 'help', 'quit', 'exit' for getting help.");
}

function HttpResponseHandler(context, event) {
    // if(event.geturl === "http://ip-api.com/json")
    context.sendResponse(event.getresp);
}

function DbGetHandler(context, event) {
    context.sendResponse("testdbput keyword was last get by:" + event.dbval);
}

function DbPutHandler(context, event) {
    context.sendResponse("testdbput keyword was last put by:" + event.dbval);
}
