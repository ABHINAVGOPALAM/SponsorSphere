from flask import Flask , render_template , request , redirect , url_for , flash , session
from app import app
from models import db, User , Sponsor , Influencer , Campaign , Rating
from werkzeug.security import generate_password_hash , check_password_hash
from functools import wraps
from datetime import date


# decorator for checjing if user is logged in
def loggedin(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first')
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return wrap


# Login and Registration Routes
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
    session['role'] = user.role

    if user.role == 'admin':
        return redirect(url_for('admin'))
    if user.role == 'sponsor':
        return redirect(url_for('sponsor'))
    if user.role == 'influencer':
        return redirect(url_for('influencer'))
    


    return redirect(url_for('login'))

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
    return ''

# Sponsor Crud


@app.route('/admin')
@loggedin
def admin():
    return render_template('admin/home.html',user= User.query.filter_by(role="admin").first())



@app.route('/sponsor')
@loggedin
def sponsor():
    user = User.query.filter_by(id=session['user_id']).first()
    sponsor = Sponsor.query.filter_by(id=session['user_id']).first()
    return render_template('sponsor/home.html',user=user,sponsor=sponsor)

@app.route('/influencer')
@loggedin
def influencer():
    user = User.query.filter_by(id=session['user_id']).first()
    influencer = Influencer.query.filter_by(id=session['user_id']).first()
    return render_template('influencer/home.html',user=user,influencer=influencer)


@app.route('/profile')
@loggedin
def profile():
    user = User.query.filter_by(id=session['user_id']).first()
    return render_template('profile.html',user=user)

@app.route('/campaigns')
@loggedin
def campaigns():
    user = User.query.filter_by(id=session['user_id']).first()
    return render_template('sponsor/campaigns/all.html',user=user)

@app.route('/campaigns/add')
@loggedin
def add_campaigns():
    user = User.query.filter_by(id=session['user_id']).first()
    return render_template('sponsor/campaigns/add.html',user=user)
@app.route('/campaigns/add' , methods=['POST'])
@loggedin
def add_campaign():
    name = request.form.get('name')
    about = request.form.get('about')
    start_date = date.fromisoformat(request.form.get('start_date'))
    end_date = date.fromisoformat(request.form.get('end_date'))
    budget = request.form.get('budget')
    visibility = request.form.get('visibility')
    if not name or not about or not start_date or not end_date or not budget:
        flash('All fields are required')
        return redirect(url_for('campaigns'))
    
    user = User.query.filter_by(id=session['user_id']).first()
    sponsor = Sponsor.query.filter_by(id=session['user_id']).first()
    niche = sponsor.niche
    new_campaign = Campaign(
        name=name,
        about=about,
        start_date=start_date,
        end_date=end_date,
        budget=budget,
        user_id=user.id,
        niche=niche,
        visibility=visibility
  )
    db.session.add(new_campaign)
    db.session.commit()
    return redirect(url_for('campaigns'))
@app.route('/campaigns/edit/<int:campaign_id>')
@loggedin
def edit_campaigns(campaign_id):
    user = User.query.filter_by(id=session['user_id']).first()
    campaign = Campaign.query.filter_by(id=campaign_id).first()
    return render_template('sponsor/campaigns/edit.html',user=user,campaign=campaign)
@app.route('/campaigns/edit/<int:campaign_id>' , methods=['POST'])
@loggedin
def edit_campaign(campaign_id):
    name = request.form.get('name')
    about = request.form.get('about')
    start_date = date.fromisoformat(request.form.get('start_date'))
    end_date = date.fromisoformat(request.form.get('end_date'))
    budget = request.form.get('budget')
    if not name  or not start_date or not end_date or not budget:
        flash('All fields are required')
        return redirect(url_for('campaigns'))

    campaign = Campaign.query.filter_by(id=campaign_id).first()

    campaign.name=name
    campaign.about=about
    campaign.start_date=start_date
    campaign.end_date=end_date
    campaign.budget=budget

    db.session.commit()
    return redirect(url_for('campaigns'))


@app.route('/stats')
@loggedin
def stats():
    pass

@app.route('/find')
@loggedin
def find():
    pass    

@app.route('/info')
@loggedin

def info():
    pass




















