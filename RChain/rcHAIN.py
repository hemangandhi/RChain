#port 5000 by default
import os
import json
import arky_utils
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

app = Flask(__name__)

def post_to_HTML(post, wrapping = "<li>", kids_wrapping = "<ol>"):
    def close(wrapping):
        return wrapping[0] + '/' + wrapping[1:]

    acc = post['content']
    acc += "<br/>\nThis post has " + str(post['votes']) + " votes"
    acc += ' <a onclick="upvote(' + str(post['id']) + ')" class="upvote" href="#" data-id="' + str(post['id']) + '">upvote</a>'
    acc += ' <a onclick="downvote(' + str(post['id']) + ')" class="downvote" href="#" data-id="' + str(post['id']) + '">downvote</a>'
    acc += ' <span id="spun' + str(post['id']) + '"><a id="reploy' + str(post['id'])+ '" onclick="openreply(' + str(post['id']) + ')" class="reply" href="#" data-id="' + str(post['id']) + '">reply</a></span>'
    acc += kids_wrapping + '\n'+ '\n'.join(post_to_HTML(k, wrapping, kids_wrapping) for k in post['kids']) + close(kids_wrapping)
    return wrapping + acc + close(wrapping)

def render_all_threads():
    return '<ol>' + ''.join(post_to_HTML(p) for p in arky_utils.all_threads()) + '</ol>\n'

@app.route('/')
def read_all():
    return """<!DOCTYPE html>
<html>
    <head>
    <script src="static/vote.js"></script>
        <title>RChain</title>
    </head>
    <body><img id="logo" src="static/RChainLogo.png" height="150" alt="RChain"/>""" + render_all_threads() + '\t</body>\n</html>'

@app.route('/upvote/<id>')
def upvote(id):
    #do
    pass

app.run()