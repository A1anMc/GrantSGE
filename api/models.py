from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Grant(Base):
    """Grant model."""
    __tablename__ = 'grants'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    funder = Column(String(255), nullable=False)
    source_url = Column(String(512))
    due_date = Column(DateTime)
    amount_string = Column(String(100))
    description = Column(Text)
    status = Column(String(50))
    eligibility_analysis = Column(Text)
    eligibility_score = Column(Float)
    last_analysis = Column(DateTime)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    last_scraped_at = Column(DateTime)
    org_id = Column(Integer, ForeignKey('organisation_profiles.id'))

    org_profile = relationship("OrganisationProfile", back_populates="grants")

class OrganisationProfile(Base):
    """Organization profile model."""
    __tablename__ = 'organisation_profiles'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    mission = Column(Text)
    focus_areas = Column(Text)
    years_active = Column(Integer)
    annual_budget = Column(String(100))
    previous_grants = Column(Text)
    staff_size = Column(Integer)
    target_demographics = Column(Text)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    grants = relationship("Grant", back_populates="org_profile") 