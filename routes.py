from flask import Flask , render_template , request , redirect , url_for , flash , session
from app import app
from models import db, User , Sponsor , Influencer , Campaign , Rating
from werkzeug.security import generate_password_hash , check_password_hash
from functools import wraps

def loggedin(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first')
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return wrap



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/register_sponsor')
def register_sponsor():
    return render_template('s_register.html')

@app.route('/register_influencer')
def register_influencer():
    return render_template('i_register.html')

@app.route('/register_sponsor', methods=['POST'])
def register_sponsor_post():
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    oraganization_name = request.form.get('organization_name')
    niche = request.form.get('niche')

    if not username or not password or not confirm_password or not oraganization_name or not niche:
        flash('All fields are required')
        return redirect(url_for('register_sponsor'))

    old_user = User.query.filter_by(username=username).first()

    if old_user:
        flash('Username already exists')
        return redirect(url_for('register_sponsor'))
    
    if password != confirm_password:
        flash('Passwords do not match')
        return redirect(url_for('register_sponsor'))
    
    password_hash = generate_password_hash(password)

    new_user = Sponsor(
        
        username=username,
        password_hash=password_hash,
        role="sponsor",
        organization_name = oraganization_name,
        niche = niche

    )    

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('login'))   

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
    flash('Logged in successfully')
    session['user_id'] = user.id
    if user.role == 'admin':
        return redirect(url_for('admin'))
    if user.role == 'sponsor':
        return redirect(url_for('sponsor'))
    if user.role == 'influencer':
        return redirect(url_for('influencer'))
    


    return redirect(url_for('login'))


@app.route('/admin')
@loggedin
def admin():
    return render_template('admin.html',user= User.query.filter_by(role="admin").first())

@app.route('/sponsor')
@loggedin
def sponsor():
    user = User.query.filter_by(id=session['user_id']).first()
    sponsor = Sponsor.query.filter_by(user_id=session['user_id']).first()

    return render_template('sponsor/home.html',user=user,sponsor=sponsor)

@app.route('/influencer') 
@loggedin  
def influencer():
    user = User.query.filter_by(id=session['user_id']).first()
    influencer = Influencer.query.filter_by(user_id=session['user_id']).first()

    return render_template('influencer.html',user=user,influencer=influencer)

@app.route('/home')
@loggedin
def home():
    user = User.query.filter_by(id=session['user_id']).first()
    if user.role == 'admin':
        return redirect(url_for('admin'))
    if user.role == 'sponsor':
        return redirect(url_for('sponsor'))
    if user.role == 'influencer':
        return redirect(url_for('influencer') )  
    return render_template('home.html',user=user)

@app.route('/profile')
@loggedin
def profile():
    user = User.query.filter_by(id=session['user_id']).first()
    return render_template('profile.html',user=user)

@app.route('/campaigns')
@loggedin
def campaigns():
    user = User.query.filter_by(id=session['user_id']).first()
    return render_template('campaigns.html',user=user)