from flask import Flask , render_template , request , redirect , url_for
from app import app
from models import User , Sponsor , Influencer , Campaign , Rating


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register_sponsor')
def register_sponsor():
    return render_template('s_register.html')

@app.route('/register_influencer')
def register_influencer():
    return render_template('i_register.html')