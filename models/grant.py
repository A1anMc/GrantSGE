from . import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON

class Grant(db.Model):
    __tablename__ = 'grants'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    funder = db.Column(db.String(200), nullable=False)
    source_url = db.Column(db.String(500))
    due_date = db.Column(db.DateTime)
    amount_string = db.Column(db.String(100))  # Store as string to handle ranges and complex amounts
    description = db.Column(db.Text)
    status = db.Column(db.String(50), default='potential')  # potential, active, closed, etc.
    eligibility_analysis = db.Column(JSON)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_scraped_at = db.Column(db.DateTime)  # For tracking when the grant was last updated from source
    
    def __repr__(self):
        return f'<Grant {self.name} by {self.funder}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'funder': self.funder,
            'source_url': self.source_url,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'amount_string': self.amount_string,
            'description': self.description,
            'status': self.status,
            'eligibility_analysis': self.eligibility_analysis
        } 