from flask_sqlalchemy import SQLAlchemy
from enum import Enum
from app import app

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer,autoincrement=True, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True,)
    password_hash = db.Column(db.String(512), nullable=False)
    role = db.Column(db.Enum('admin', 'sponsor', 'influencer'), nullable=False)
    flag = db.Column(db.Boolean, default=False)
    # is_admin = db.Column(db.Boolean, default=False)
    
    # relationships
    influencers = db.relationship("Influencer", backref="user", lazy=True)# only loaded when needed
    
    campaigns = db.relationship("Campaign", backref="user", cascade="all, delete-orphan")
    ratings = db.relationship("Rating", backref="user", cascade="all, delete-orphan")

class Sponsor(User):
    __tablename__ = "sponsor"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    organization_name = db.Column(db.String(120), nullable=False)
    niche = db.Column(db.String(120), nullable=False)
    total_budget = db.Column(db.Float, nullable=False)
    flag = db.Column(db.Boolean, default=False)
    
    # relationships
    campaigns = db.relationship("Campaign", backref="sponsor", cascade= "all, delete-orphan")

class Influencer(User):
    __tablename__ = "influencer"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    platform = db.Column(db.String(120), nullable=False)
    niche = db.Column(db.String(120), nullable=False)
    reach = db.Column(db.Integer, nullable=False)
    flag = db.Column(db.Boolean, default=False)

    # relationships

    ad_requests = db.relationship("AdRequest", backref="influencer", cascade="all, delete-orphan")
    ratings = db.relationship("Rating", backref="influencer", cascade="all, delete-orphan")

class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsor.id'), nullable=False)
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
    influencer_id = db.Column(db.Integer, db.ForeignKey('influencer.id'), nullable=False)
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
    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsor.id'), nullable=False)
    influencer_id = db.Column(db.Integer, db.ForeignKey('influencer.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)