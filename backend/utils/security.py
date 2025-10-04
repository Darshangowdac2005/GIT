# backend/utils/security.py
import os
from functools import wraps
from flask import request, jsonify
import jwt # Placeholder for actual JWT library

# --- Placeholders ---
SECRET_KEY = os.getenv('JWT_SECRET', 'test_secret')

def hash_password(password):
    # Should use bcrypt.hashpw(password, bcrypt.gensalt())
    return password # Placeholder

def verify_password(password, hashed_password):
    # Should use bcrypt.checkpw(password, hashed_password)
    return password == hashed_password # Placeholder

def encode_auth_token(user_id, role):
    try:
        payload = {'user_id': user_id, 'role': role}
        return jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    except Exception as e:
        return str(e)

# --- Authentication Decorator ---
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or not token.startswith('Bearer '):
            return jsonify({'message': 'Token is missing or invalid!'}), 401
        
        token = token.split(' ')[1]
        
        try:
            # Decode token and attach user info to request
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.user_id = data['user_id']
            request.user_role = data['role']
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
            
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    @token_required
    def decorated(*args, **kwargs):
        if request.user_role != 'admin':
            return jsonify({'message': 'Admin access required!'}), 403
        return f(*args, **kwargs)
    return decorated