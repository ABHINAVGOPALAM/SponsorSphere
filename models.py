from flask_sqlalchemy import SQLAlchemy
from enum import Enum
from app import app
from werkzeug.security import generate_password_hash , check_password_hash

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer,autoincrement=True, primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    password_hash = db.Column(db.String(512), nullable=False)
    role = db.Column(db.Enum('admin', 'sponsor', 'influencer'), nullable=False)
    flag = db.Column(db.Boolean, default=False)
    # is_admin = db.Column(db.Boolean, default=False)

    __mapped_args__ ={
        'polymorphic_on': role
        #'polymorphic_identity': 'user'  
    }
    
    # relationships
    influencers = db.relationship("Influencer", backref='user', lazy=True)# only loaded when needed
    
    campaigns = db.relationship("Campaign", backref="user", cascade="all, delete-orphan")
    ratings = db.relationship("Rating", backref="user", cascade="all, delete-orphan")

class Sponsor(User):
    __tablename__ = "sponsor"
    sponsor_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    organization_name = db.Column(db.String(120), nullable=False)
    niche = db.Column(db.String(120), nullable=False)
    total_budget = db.Column(db.Float, default=0.0)
    
    __mapped_args__ ={
        'polymorphic_identity': 'sponsor'
    }

    # relationships
    campaigns = db.relationship("Campaign", backref="sponsor", cascade= "all, delete-orphan")

class Influencer(User):
    __tablename__ = "influencer"
    influencer_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(120), nullable=True)
    platform = db.Column(db.String(120), nullable=False)
    niche = db.Column(db.String(120), nullable=False)
    followers = db.Column(db.Integer, nullable=False)

    __mapped_args__ ={
        'polymorphic_identity': 'influencer'
    }
    # relationships
    ad_requests = db.relationship("AdRequest", backref="influencer", cascade="all, delete-orphan")
    ratings = db.relationship("Rating", backref="influencer", cascade="all, delete-orphan")

class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    about = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    budget = db.Column(db.Float, nullable=False)
    niche = db.Column(db.String(120), nullable=False)
    visibility = db.Column(db.Enum('public', 'private'), nullable=False)
    flag = db.Column(db.Boolean, default=False)
    
    ad_requests = db.relationship("AdRequest", backref="campaign", cascade="all, delete-orphan")


class AdRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
    influencer_id = db.Column(db.Integer, db.ForeignKey('influencer.influencer_id'), nullable=False)
    messages = db.Column(db.Text, nullable=False)
    requirements = db.Column(db.Text, nullable=False)
    payment_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.Enum('pending', 'accepted', 'rejected'), nullable=False)


class Statistics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total_users = db.Column(db.Integer, nullable=False)
    total_campaigns = db.Column(db.Integer, nullable=False)
    total_ad_requests = db.Column(db.Integer, nullable=False)
    flagged_users = db.Column(db.Integer, nullable=False)

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsor.sponsor_id'), nullable=False)
    influencer_id = db.Column(db.Integer, db.ForeignKey('influencer.influencer_id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

with app.app_context():
    db.create_all()

    user = User.query.filter_by(role="admin").first()
    if not user:
        sys_admin = User(username="admin",password_hash= generate_password_hash("admin"),role="admin",)
        db.session.add(sys_admin)
        db.session.commit()

