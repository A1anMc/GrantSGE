import pytest
import json
import asyncio
from unittest.mock import patch, MagicMock, Mock
from datetime import datetime
from api.ai_core import (
    run_eligibility_scan,
    parse_ai_response,
    construct_eligibility_prompt,
    EligibilityAnalysis,
    EligibilityCriterion
)
from api.models import Grant, OrganisationProfile
from api.database import init_db

@pytest.fixture(scope='session')
def db_engine():
    """Create test database."""
    engine = init_db()
    yield engine
    # Clean up
    import os
    if os.path.exists('grants.db'):
        os.remove('grants.db')

@pytest.fixture
def mock_grant():
    """Create a mock grant."""
    grant = Mock(name="Test Grant")
    grant.name = "Test Grant"
    grant.funder = "Test Funder"
    grant.description = "Test Description"
    grant.amount_string = "$10,000"
    grant.due_date = datetime.now()
    grant.org_id = 1
    return grant

@pytest.fixture
def mock_org_profile():
    """Create a mock organization profile."""
    org = Mock(name="Test Org")
    org.name = "Test Organization"
    org.mission = "Test Mission"
    org.focus_areas = "Education, Health"
    org.years_active = 5
    org.annual_budget = "$500,000"
    org.previous_grants = "Grant A, Grant B"
    org.staff_size = 10
    org.target_demographics = "Youth, Seniors"
    return org

@pytest.fixture
def sample_ai_response():
    """Sample AI response."""
    return {
        "score": 0.85,
        "alignment_points": ["Strong education focus", "Appropriate budget size"],
        "disqualifiers": ["Limited track record"],
        "missing_info": ["Detailed project plan"],
        "criteria": [
            {
                "name": "Organization Size",
                "met": True,
                "description": "Organization meets size requirements"
            },
            {
                "name": "Budget Requirements",
                "met": True,
                "description": "Budget is within acceptable range"
            }
        ]
    }

@pytest.mark.asyncio
async def test_run_eligibility_scan_success(mock_grant, mock_org_profile, sample_ai_response):
    """Test successful eligibility scan."""
    with patch('api.ai_core.get_db_session') as mock_db, \
         patch('anthropic.Anthropic') as mock_anthropic:

        # Setup mock database session
        mock_session = MagicMock()
        mock_db.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.side_effect = [mock_grant, mock_org_profile]

        # Setup mock API client
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text=json.dumps(sample_ai_response))]
        mock_client.messages.create.return_value = mock_response

        result = await run_eligibility_scan(1)
        assert result['score'] == 0.85
        assert len(result['alignment_points']) == 2
        assert len(result['criteria']) == 2

@pytest.mark.asyncio
async def test_run_eligibility_scan_cached(mock_grant, sample_ai_response):
    """Test cached eligibility scan results."""
    with patch('api.utils.Cache.get', return_value=sample_ai_response):
        result = await run_eligibility_scan(1)
        assert result == sample_ai_response

@pytest.mark.asyncio
async def test_run_eligibility_scan_rate_limited():
    """Test rate limiting."""
    with patch('api.utils.RateLimiter.is_rate_limited', return_value=True):
        with pytest.raises(Exception) as exc:
            await run_eligibility_scan(1)
        assert "Rate limit exceeded" in str(exc.value)

def test_parse_ai_response_valid(sample_ai_response):
    """Test parsing valid AI response."""
    response = json.dumps(sample_ai_response)
    result = parse_ai_response(response)
    assert result['score'] == 0.85
    assert len(result['alignment_points']) == 2
    assert len(result['criteria']) == 2

def test_parse_ai_response_invalid():
    """Test parsing invalid AI response."""
    invalid_response = "{invalid json}"
    with pytest.raises(ValueError):
        parse_ai_response(invalid_response)

def test_construct_eligibility_prompt(mock_grant, mock_org_profile):
    """Test prompt construction."""
    prompt = construct_eligibility_prompt(mock_grant, mock_org_profile)
    assert "Test Grant" in prompt
    assert "Test Organization" in prompt
    assert "Education, Health" in prompt

def test_eligibility_analysis_model():
    """Test EligibilityAnalysis model validation."""
    data = {
        "score": 0.85,
        "alignment_points": ["Point 1"],
        "disqualifiers": ["Issue 1"],
        "missing_info": ["Info 1"],
        "criteria": [
            {
                "name": "Criterion 1",
                "met": True,
                "description": "Description 1"
            }
        ]
    }
    analysis = EligibilityAnalysis(**data)
    assert analysis.score == 0.85
    assert len(analysis.criteria) == 1

def test_eligibility_criterion_model():
    """Test EligibilityCriterion model validation."""
    data = {
        "name": "Test Criterion",
        "met": True,
        "description": "Test Description"
    }
    criterion = EligibilityCriterion(**data)
    assert criterion.name == "Test Criterion"
    assert criterion.met is True 