from flask import Flask , render_template , request , redirect , url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

import config

import models

@app.route('/login')
def index():
    return render_template('login.html')




