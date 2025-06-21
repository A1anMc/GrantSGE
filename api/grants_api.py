from flask import Blueprint, jsonify, request
from models import db
from models.grant import Grant
from models.organisation import OrganisationProfile
from api.ai_core import run_eligibility_scan, get_db_session, anthropic
from datetime import datetime
from typing import Dict, Any
from sqlalchemy.exc import SQLAlchemyError
import logging
import asyncio
from api.monitoring import track_timing, DRAFT_REQUESTS, DRAFT_LATENCY

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Blueprint
grants_bp = Blueprint('grants', __name__)

def validate_grant_data(data: Dict[str, Any]) -> tuple[bool, str]:
    """Validate grant data from request."""
    required_fields = ['name', 'funder']
    
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"
            
    return True, ""

@grants_bp.route('/api/grants', methods=['GET'])
def get_grants():
    """Get all grants with optional filtering."""
    try:
        # Get query parameters for filtering
        status = request.args.get('status')
        funder = request.args.get('funder')
        
        # Start with base query
        query = Grant.query
        
        # Apply filters if provided
        if status:
            query = query.filter(Grant.status == status)
        if funder:
            query = query.filter(Grant.funder == funder)
            
        # Execute query and convert to list of dictionaries
        grants = [grant.to_dict() for grant in query.all()]
        
        return jsonify({
            'success': True,
            'data': grants,
            'count': len(grants)
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching grants: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to fetch grants'
        }), 500

@grants_bp.route('/api/grants/<int:grant_id>', methods=['GET'])
def get_grant(grant_id):
    """Get a specific grant by ID."""
    try:
        grant = Grant.query.get(grant_id)
        
        if not grant:
            return jsonify({
                'success': False,
                'error': 'Grant not found'
            }), 404
            
        return jsonify({
            'success': True,
            'data': grant.to_dict()
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching grant {grant_id}: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to fetch grant'
        }), 500

@grants_bp.route('/api/grants', methods=['POST'])
def create_grant():
    """Create a new grant."""
    try:
        data = request.get_json()
        
        # Validate request data
        is_valid, error_message = validate_grant_data(data)
        if not is_valid:
            return jsonify({
                'success': False,
                'error': error_message
            }), 400
            
        # Create new grant
        new_grant = Grant(
            name=data['name'],
            funder=data['funder'],
            source_url=data.get('source_url'),
            due_date=datetime.fromisoformat(data['due_date']) if data.get('due_date') else None,
            amount_string=data.get('amount_string'),
            description=data.get('description'),
            status=data.get('status', 'potential'),
            eligibility_analysis=data.get('eligibility_analysis', {})
        )
        
        db.session.add(new_grant)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': new_grant.to_dict(),
            'message': 'Grant created successfully'
        }), 201
        
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Database error creating grant: {e}")
        return jsonify({
            'success': False,
            'error': 'Database error occurred'
        }), 500
    except Exception as e:
        logger.error(f"Error creating grant: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to create grant'
        }), 500

@grants_bp.route('/api/grants/<int:grant_id>', methods=['PUT'])
def update_grant(grant_id):
    """Update an existing grant."""
    try:
        grant = Grant.query.get(grant_id)
        
        if not grant:
            return jsonify({
                'success': False,
                'error': 'Grant not found'
            }), 404
            
        data = request.get_json()
        
        # Update fields if provided in request
        if 'name' in data:
            grant.name = data['name']
        if 'funder' in data:
            grant.funder = data['funder']
        if 'source_url' in data:
            grant.source_url = data['source_url']
        if 'due_date' in data:
            grant.due_date = datetime.fromisoformat(data['due_date']) if data['due_date'] else None
        if 'amount_string' in data:
            grant.amount_string = data['amount_string']
        if 'description' in data:
            grant.description = data['description']
        if 'status' in data:
            grant.status = data['status']
        if 'eligibility_analysis' in data:
            grant.eligibility_analysis = data['eligibility_analysis']
            
        grant.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': grant.to_dict(),
            'message': 'Grant updated successfully'
        }), 200
        
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Database error updating grant {grant_id}: {e}")
        return jsonify({
            'success': False,
            'error': 'Database error occurred'
        }), 500
    except Exception as e:
        logger.error(f"Error updating grant {grant_id}: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to update grant'
        }), 500

# Additional helper endpoints

@grants_bp.route('/api/grants/search', methods=['GET'])
def search_grants():
    """Search grants with more complex filtering."""
    try:
        # Get search parameters
        keyword = request.args.get('keyword', '').lower()
        min_date = request.args.get('min_date')
        max_date = request.args.get('max_date')
        
        # Start with base query
        query = Grant.query
        
        # Apply filters
        if keyword:
            query = query.filter(
                db.or_(
                    Grant.name.ilike(f'%{keyword}%'),
                    Grant.description.ilike(f'%{keyword}%'),
                    Grant.funder.ilike(f'%{keyword}%')
                )
            )
            
        if min_date:
            query = query.filter(Grant.due_date >= datetime.fromisoformat(min_date))
        if max_date:
            query = query.filter(Grant.due_date <= datetime.fromisoformat(max_date))
            
        # Execute query
        grants = [grant.to_dict() for grant in query.all()]
        
        return jsonify({
            'success': True,
            'data': grants,
            'count': len(grants)
        }), 200
        
    except Exception as e:
        logger.error(f"Error searching grants: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to search grants'
        }), 500

@grants_bp.route('/grants/<int:grant_id>/analyze-eligibility', methods=['POST'])
async def analyze_grant_eligibility(grant_id):
    """
    Trigger an AI-powered eligibility analysis for a specific grant.
    """
    try:
        # Run the eligibility scan
        analysis_result = await run_eligibility_scan(grant_id)
        
        return jsonify({
            'status': 'success',
            'analysis': analysis_result
        }), 200
        
    except ValueError as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 404
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f"Failed to analyze grant eligibility: {str(e)}"
        }), 500

@grants_bp.route('/api/grants/<int:grant_id>/generate-draft', methods=['POST'])
@track_timing('total')
async def generate_grant_draft(grant_id):
    """
    Generate an AI-powered draft for a grant application question.
    """
    try:
        # Start timing
        DRAFT_LATENCY.labels(phase='total').observe(0)
        
        # Get database session
        db = get_db_session()
        
        try:
            # Validate request data
            data = request.get_json()
            if not data or 'application_question' not in data:
                return jsonify({
                    'success': False,
                    'error': 'Missing required field: application_question'
                }), 400
                
            # Get the grant
            grant = db.query(Grant).filter(Grant.id == grant_id).first()
            if not grant:
                return jsonify({
                    'success': False,
                    'error': 'Grant not found'
                }), 404
                
            # Get organization profile
            org_profile = db.query(OrganisationProfile).first()
            if not org_profile:
                return jsonify({
                    'success': False,
                    'error': 'No organization profile found'
                }), 404
                
            # Construct the prompt
            prompt = f"""You are an expert grant writer. Write a compelling response to the following grant application question.
Use the provided context about the grant and organization to craft a detailed, persuasive answer.

GRANT DETAILS:
Name: {grant.name}
Funder: {grant.funder}
Description: {grant.description}
Amount: {grant.amount_string}

ORGANIZATION PROFILE:
Name: {org_profile.name}
Mission: {org_profile.mission}
Focus Areas: {org_profile.focus_areas}
Years Active: {org_profile.years_active}
Annual Budget: {org_profile.annual_budget}
Previous Grants: {org_profile.previous_grants}
Staff Size: {org_profile.staff_size}
Target Demographics: {org_profile.target_demographics}

ADDITIONAL CONTEXT:
{data.get('context_documents', '')}

APPLICATION QUESTION:
{data['application_question']}

Please write a response that:
1. Directly addresses the question asked
2. Uses specific examples and metrics from the organization's profile
3. Aligns the organization's strengths with the grant's objectives
4. Maintains a professional yet engaging tone
5. Follows any word or character limits specified in the question
6. Includes relevant achievements and impact data
7. Demonstrates clear understanding of the funder's priorities

Your response should be well-structured with clear paragraphs and should not include any placeholder text or notes.
"""
            
            # Call the Anthropic API with retry logic
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    @track_timing('api_call')
                    async def make_api_call():
                        DRAFT_LATENCY.labels(phase='api_call').observe(0)
                        return anthropic.messages.create(
                            model="claude-3-opus-20240229",
                            max_tokens=4000,
                            temperature=0.7,
                            system="You are an expert grant writer with extensive experience in crafting successful grant applications. Write clear, compelling, and evidence-based responses.",
                            messages=[
                                {
                                    "role": "user",
                                    "content": prompt
                                }
                            ]
                        )
                    
                    response = await make_api_call()
                    break
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    logger.warning(f"API call failed (attempt {attempt + 1}): {str(e)}")
                    await asyncio.sleep(1 * (attempt + 1))
            
            # Record success
            DRAFT_REQUESTS.labels(status='success').inc()
            
            return jsonify({
                'success': True,
                'data': {
                    'draft_text': response.content[0].text.strip()
                }
            }), 200
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Error generating grant draft: {str(e)}", exc_info=True)
        # Record error
        DRAFT_REQUESTS.labels(status='error').inc()
        return jsonify({
            'success': False,
            'error': f"Failed to generate grant draft: {str(e)}"
        }), 500 