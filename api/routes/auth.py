from flask import Blueprint, request, jsonify
from api.models.user import User
from api.auth import (
    create_user_token,
    revoke_token,
    rate_limit,
    role_required
)
from api.database import db
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import (
    jwt_required,
    get_jwt,
    current_user
)

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/auth/register', methods=['POST'])
@rate_limit(limit=10, period=3600)  # 10 registrations per hour
def register():
    """Register a new user."""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['email', 'password', 'first_name', 'last_name']
        if not all(field in data for field in required_fields):
            return jsonify({
                'success': False,
                'error': 'Missing required fields'
            }), 400

        # Create new user
        user = User(
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            roles=['user']  # Default role
        )
        user.set_password(data['password'])

        db.session.add(user)
        db.session.commit()

        # Create access token
        token = create_user_token(user.id, user.roles)

        return jsonify({
            'success': True,
            'data': {
                'user': user.to_dict(),
                'token': token
            }
        }), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Email already exists'
        }), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@auth_bp.route('/api/auth/login', methods=['POST'])
@rate_limit(limit=100, period=3600)  # 100 login attempts per hour
def login():
    """Login user."""
    try:
        data = request.get_json()
        
        if not data.get('email') or not data.get('password'):
            return jsonify({
                'success': False,
                'error': 'Email and password required'
            }), 400

        user = User.query.filter_by(email=data['email']).first()

        if not user or not user.check_password(data['password']):
            return jsonify({
                'success': False,
                'error': 'Invalid email or password'
            }), 401

        if not user.is_active:
            return jsonify({
                'success': False,
                'error': 'Account is disabled'
            }), 403

        # Update last login
        user.last_login = datetime.utcnow()
        db.session.commit()

        # Create access token
        token = create_user_token(user.id, user.roles)

        return jsonify({
            'success': True,
            'data': {
                'user': user.to_dict(),
                'token': token
            }
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@auth_bp.route('/api/auth/logout', methods=['POST'])
@jwt_required()
def logout():
    """Logout user."""
    try:
        jti = get_jwt()["jti"]
        revoke_token(jti, get_jwt()["exp"])
        
        return jsonify({
            'success': True,
            'message': 'Successfully logged out'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@auth_bp.route('/api/auth/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current user info."""
    return jsonify({
        'success': True,
        'data': current_user.to_dict()
    }), 200

@auth_bp.route('/api/auth/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """Change user password."""
    try:
        data = request.get_json()
        
        if not data.get('current_password') or not data.get('new_password'):
            return jsonify({
                'success': False,
                'error': 'Current and new password required'
            }), 400

        if not current_user.check_password(data['current_password']):
            return jsonify({
                'success': False,
                'error': 'Current password is incorrect'
            }), 401

        current_user.set_password(data['new_password'])
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Password updated successfully'
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@auth_bp.route('/api/auth/users', methods=['GET'])
@jwt_required()
@role_required(['admin'])
def list_users():
    """List all users (admin only)."""
    try:
        users = User.query.all()
        return jsonify({
            'success': True,
            'data': [user.to_dict() for user in users]
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500 