function upvote(id){
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function(){
        if(this.readState == 4 && this.status == 200){
            window.location.reload();
        }
    }
    xhr.open("POST", "/upvote/" + id + "/" + prompt("Enter your token!"), true);
    xhr.send();
}

function downvote(id){
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function(){
        if(this.readState == 4 && this.status == 200){
            window.location.reload();
        }
    }
    xhr.open("POST", "/downvote/" + id + "/" + prompt("Enter your token!"), true);
    xhr.send();
}

function openreply(hash){
	document.getElementById("textin") = null;
	document.getElementById("reploy"+str(hash)).onclick = "reply(" + hash + ")";
	document.getElementById("spun").innerHTML = '<input type="text" id="textin">' + document.getElementById("spun").innerHTML;
}

function reply(hash){


}
