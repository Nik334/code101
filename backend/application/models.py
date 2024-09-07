from .database import db
from datetime import datetime
from pytz import timezone
from flask import url_for

class Users(db.Model):
    __tablename__="Users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, unique=True, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    user_type = db.Column(db.Enum('admin', 'influencer', 'sponsor'), default='influencer')

    def influencer_bio(self):
        return InfluencerBio.query.filter_by(user_id=self.id).first()
    
    def sponsor_bio(self):
        return SponsorBio.query.filter_by(user_id=self.id).first()
    
    def serialize(self):   
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'user_type': self.user_type
        }
    
class InfluencerBio(db.Model):
    __tablename__="Influencer_Bio"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    niche = db.Column(db.String, nullable=False)
    ads = db.relationship("Ads", backref=db.backref("influencer", lazy=True), cascade="all, delete-orphan")

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'niche': self.niche
        }
    
class SponsorBio(db.Model):
    __tablename__="Sponsor_Bio"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    industry = db.Column(db.String, nullable=False)
    budget = db.Column(db.Integer, nullable=False)
    approved = db.Column(db.Boolean, default=True)
    campaigns = db.relationship("Campaigns", backref=db.backref("sponsor", lazy=True), cascade="all, delete-orphan")

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'industry': self.industry,
            'budget': self.budget,
            'approved': self.approved
        }
    
class Campaigns(db.Model):
    __tablename__="Campaigns"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sponsor_id = db.Column(db.Integer, db.ForeignKey('Sponsor_Bio.id'))
    campaign_name = db.Column(db.String, nullable=False)
    campaign_desc = db.Column(db.String, nullable=False)
    campaign_budget = db.Column(db.Integer, nullable=False)
    campaign_start = db.Column(db.DateTime, nullable=False)
    campaign_end = db.Column(db.DateTime, nullable=False)
    flagged = db.Column(db.Boolean, default=False)
    campaign_visibility = db.Column(db.Enum('public', 'private'), default='public')
    influencer_id = db.Column(db.Integer,db.ForeignKey
    ('Influencer_Bio.id'))
    campaign_goal = db.Column(db.String, nullable=False)
    ads = db.relationship("Ads", backref=db.backref("campaign", lazy=True), cascade="all, delete-orphan")

    def serialize(self):
        return {
            'id': self.id,
            'campaign_name': self.campaign_name,
            'campaign_desc': self.campaign_desc,
            'campaign_budget': self.campaign_budget,
            'campaign_start': self.campaign_start,
            'campaign_end': self.campaign_end,
            'campaign_visibility': self.campaign_visibility,
            'influencer_id':self.influencer_id,
            'campaign_goal': self.campaign_goal
        }
    
class Ads(db.Model):
    __tablename__="Ads"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('Campaigns.id'))
    influencer_id = db.Column(db.Integer, db.ForeignKey('Influencer_Bio.id'))
    messages = db.Column(db.String, nullable=False)
    requirements = db.Column(db.String, nullable=False)
    payment_amount = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Enum('accepted', 'pending', 'rejected'), default='pending')
    negotiation_turn= db.Column(db.Enum('influencer', 'sponsor'), default='influencer')

    def serialize(self):
        return {
            'id': self.id,
            'messages': self.messages,
            'requirements': self.requirements,
            'payment_amount': self.payment_amount,
            'status': self.status,
            'negotiation_turn': self.negotiation_turn
        }