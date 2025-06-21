from typing import Dict, Any, List
import os
import logging
import asyncio
from anthropic import Anthropic
from sqlalchemy.orm import Session
from models.grant import Grant
from models.organisation import OrganisationProfile
from models.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from .utils import rate_limit, cache_result, get_db_session
from pydantic import BaseModel, Field, validator
from .monitoring import track_timing, set_model_info, update_system_metrics, ELIGIBILITY_REQUESTS
from .cache_manager import cached
import json

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Anthropic client
anthropic = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

# Set model info for monitoring
set_model_info("claude-3-opus", "20240229")

class EligibilityCriterion(BaseModel):
    """Model for individual eligibility criteria."""
    name: str
    met: bool
    description: str

    @validator('name')
    def name_not_empty(cls, v):
        """Validate that name is not empty."""
        if not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()

class EligibilityAnalysis(BaseModel):
    """Model for grant eligibility analysis."""
    score: float
    alignment_points: List[str]
    disqualifiers: List[str]
    missing_info: List[str]
    criteria: List[EligibilityCriterion]

    @validator('score')
    def score_range(cls, v):
        """Validate score is between 0 and 1."""
        if not 0 <= v <= 1:
            raise ValueError('Score must be between 0 and 1')
        return v

    @validator('alignment_points', 'disqualifiers', 'missing_info')
    def non_empty_lists(cls, v):
        """Validate that lists have at least one item."""
        if not v:
            raise ValueError('List cannot be empty')
        return v

def construct_eligibility_prompt(grant, org_profile):
    """Construct prompt for eligibility analysis."""
    return f"""Analyze grant eligibility for:

Grant Details:
- Name: {grant.name}
- Funder: {grant.funder}
- Description: {grant.description}
- Amount: {grant.amount_string}
- Due Date: {grant.due_date}

Organization Profile:
- Name: {org_profile.name}
- Mission: {org_profile.mission}
- Focus Areas: {org_profile.focus_areas}
- Years Active: {org_profile.years_active}
- Annual Budget: {org_profile.annual_budget}
- Previous Grants: {org_profile.previous_grants}
- Staff Size: {org_profile.staff_size}
- Target Demographics: {org_profile.target_demographics}

Analyze the alignment between the grant requirements and organization profile.
Format your response in JSON with the following structure:
{{
    "score": float (0-1),
    "alignment_points": [string],
    "disqualifiers": [string],
    "missing_info": [string],
    "criteria": [
        {{
            "name": string,
            "met": boolean,
            "description": string
        }}
    ]
}}"""

def parse_ai_response(response_text: str) -> Dict:
    """Parse and validate AI response."""
    try:
        data = json.loads(response_text)
        analysis = EligibilityAnalysis(**data)
        return analysis.model_dump()
    except (json.JSONDecodeError, ValueError) as e:
        raise ValueError(f"Invalid AI response format: {str(e)}")

@cached(key_prefix='eligibility_scan')
@track_timing('eligibility_scan')
async def run_eligibility_scan(grant_id: int) -> Dict:
    """Run eligibility scan for a grant."""
    try:
        # Get grant and org data
        session = get_db_session()
        grant = session.query(Grant).filter(Grant.id == grant_id).first()
        org_profile = session.query(OrganisationProfile).filter(OrganisationProfile.id == grant.org_id).first()

        if not grant or not org_profile:
            raise ValueError("Grant or organization not found")

        # Construct prompt
        prompt = construct_eligibility_prompt(grant, org_profile)

        # Call AI API
        client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        response = await client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1500,
            temperature=0.2,
            system="You are an expert grant analyst. Analyze grant eligibility based on the provided information.",
            messages=[{"role": "user", "content": prompt}]
        )

        # Parse and validate response
        result = parse_ai_response(response.content[0].text)

        # Update grant status
        grant.last_analysis = datetime.now()
        grant.eligibility_score = result['score']
        session.commit()

        ELIGIBILITY_REQUESTS.labels(status='success').inc()
        return result

    except Exception as e:
        ELIGIBILITY_REQUESTS.labels(status='error').inc()
        raise Exception(f"Error in eligibility scan: {str(e)}")

def format_eligibility_results(analysis: Dict[str, Any]) -> str:
    """Format eligibility analysis results for display."""
    return f"""
Eligibility Analysis Results:
---------------------------
Overall Score: {analysis['score']:.2f}

Key Alignment Points:
{chr(10).join(f'- {point}' for point in analysis['alignment_points'])}

Potential Disqualifiers:
{chr(10).join(f'- {issue}' for issue in analysis['disqualifiers'])}

Missing Information:
{chr(10).join(f'- {info}' for info in analysis['missing_info'])}

Detailed Criteria:
{chr(10).join(f'- {c["name"]}: {"✓" if c["met"] else "✗"} ({c["description"]})' for c in analysis['criteria'])}
""" 