# backend/routes/category_routes.py

from flask import Blueprint, jsonify, request
from config.db_connector import db
from utils.security import admin_required

category_bp = Blueprint('category_bp', __name__)

@category_bp.route('', methods=['GET'])
def list_categories():
    cursor = db.conn.cursor(dictionary=True)
    cursor.execute("SELECT category_id, name FROM Categories ORDER BY name ASC")
    categories = cursor.fetchall()
    cursor.close()
    return jsonify(categories), 200

@category_bp.route('', methods=['POST'])
@admin_required
def create_category():
    data = request.json or {}
    name = (data.get('name') or '').strip()
    if not name:
        return jsonify({'error': 'Category name is required.'}), 400
    cursor = db.conn.cursor()
    try:
        cursor.execute("INSERT INTO Categories (name) VALUES (%s)", (name,))
        db.conn.commit()
        return jsonify({'message': 'Category created', 'category_id': cursor.lastrowid}), 201
    except Exception as err:
        db.conn.rollback()
        return jsonify({'error': f'Database error: {err}'}), 400
    finally:
        cursor.close()


