from . import db
from datetime import datetime

# Association table for many-to-many relationship between organisations and grants
org_grants = db.Table('org_grants',
    db.Column('organisation_id', db.Integer, db.ForeignKey('organisation_profiles.id'), primary_key=True),
    db.Column('grant_id', db.Integer, db.ForeignKey('grants.id'), primary_key=True),
    db.Column('tracking_status', db.String(50), default='interested'),  # e.g., 'interested', 'applying', 'submitted'
    db.Column('added_at', db.DateTime, default=datetime.utcnow)
)

class OrganisationProfile(db.Model):
    __tablename__ = 'organisation_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    abn = db.Column(db.String(11), unique=True)  # Australian Business Number
    dgr_status = db.Column(db.Boolean, default=False)
    annual_revenue = db.Column(db.Integer)
    profile_text = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship with User (one-to-one)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    user = db.relationship('User', back_populates='organisation_profile')
    
    # Relationship with Grants (many-to-many)
    tracked_grants = db.relationship('Grant',
                                   secondary=org_grants,
                                   lazy='dynamic',
                                   backref=db.backref('tracking_organisations', lazy='dynamic'))
    
    def __repr__(self):
        return f'<OrganisationProfile {self.name}>' 