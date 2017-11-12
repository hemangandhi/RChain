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
    acc += "<br/>This post has " + str(post['votes']) + " votes"
    acc += ' <a class="upvote" href="#" data-id="' + str(post['id']) + '">upvote</a>'
    acc += ' <a class="downvote" href="#" data-id="' + str(post['id']) + '">downvote</a>'
    acc += kids_wrapping + ''.join(post_to_HTML(k, wrapping, kids_wrapping) for k in post['kids']) + close(kids_wrapping)
    return wrapping + acc + close(wrapping)

def render_all_threads():
    return '<ol>' + ''.join(post_to_HTML(p) for p in arky_utils.all_threads()) + '</ol>'

@app.route('/')
def read_all():
    return """<!DOCTYPE html><html>
    <head><title>RChain</title></head><body>""" + render_all_threads() + "</body></html>"

app.run()
