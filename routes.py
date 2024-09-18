from flask import Flask , render_template , request , redirect , url_for , flash
from app import app
from models import db, User , Sponsor , Influencer , Campaign , Rating
from werkzeug.security import generate_password_hash , check_password_hash

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

@app.route('/register_influencer', methods=['POST'])
def register_influencer_post():
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    platform = request.form.get('platform')
    niche = request.form.get('niche')
    followers = request.form.get('followers')
    name = request.form.get('name')

    if not username or not password or not confirm_password or not platform  or not followers or not name:
        flash('All fields are required')
        return redirect(url_for('register_influencer'))

    old_user = User.query.filter_by(username=username).first()

    if old_user:
        flash('Username already exists')
        return redirect(url_for('register_influencer'))
    
    if password != confirm_password:
        flash('Passwords do not match')
        return redirect(url_for('register_influencer'))
    
    password_hash = generate_password_hash(password)

    new_user = Influencer(
        
        username=username,
        password_hash=password_hash,
        platform=platform,
        niche=niche,
        followers=followers,
        name = name,
        role="influencer"  
    )


    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('login'))


@app.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        flash('All fields are required')
        return redirect(url_for('login'))

    user = User.query.filter_by(username=username).first()

    if not user :
        flash('Invalid username ')
        return redirect(url_for('login'))
    if not check_password_hash(user.password_hash, password):
        flash('Invalid password')
        return redirect(url_for('login'))

    if user.role == 'admin':
        return redirect(url_for('admin'))
    if user.role == 'sponsor':
        return redirect(url_for('sponsor'))
    if user.role == 'influencer':
        return redirect(url_for('influencer'))

    return redirect(url_for('login'))


@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/sponsor')
def sponsor():
    return render_template('sponsor.html')

@app.route('/influencer')   
def influencer():
    return render_template('influencer.html')