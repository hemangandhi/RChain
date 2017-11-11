#port 5000 by default
import os
import sqlite3
import json
import arky_utils
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello world!"
