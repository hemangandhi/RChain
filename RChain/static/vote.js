function upvote(hash){


}

function downvote(hash){


}

function openreply(hash){
	document.getElementById("textin") = null;
	document.getElementById("reploy"+str(hash)).onclick = "reply(" + hash + ")";
	document.getElementById("spun").innerHTML = '<input type="text" id="textin">' + document.getElementById("spun").innerHTML;
}

function reply(hash){


}
