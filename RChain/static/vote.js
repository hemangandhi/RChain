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
	if(document.getElementById("textin") != null){
		document.getElementById(x).onclick = "openreply(" + x.substr(6) + ")";
		document.getElementById("textin").setAttribute("hidden","");
		document.removeAttribute("id");
	}
	if(document.getElementById("spun" + hash).innerHTML.match(/<input type="text"/)!=null){
		document.getElementById("spun" + hash).getElementsByClass("input").item(0).setAttribute("id","textin");
		document.getElementById("textin").removeAttribute("z");
	}
	else	document.getElementById("spun" + hash).innerHTML = '<input type="text" id="textin">' + document.getElementById("spun").innerHTML;
}
}

function reply(hash){


}
