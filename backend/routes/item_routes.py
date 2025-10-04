# backend/routes/item_routes.py

import mysql.connector
from flask import Blueprint, request, jsonify
from config.db_connector import db
from utils.security import token_required

item_bp = Blueprint('item_bp', __name__)

@item_bp.route('', methods=['POST'])
@token_required
def report_item():
    user_id = request.user_id 
    data = request.json
    title = data.get('title')
    description = data.get('description')
    status = data.get('status') 
    category_id = data.get('category_id') 
    
    # Placeholder for image_url logic
    image_url = 'N/A' 

    if not all([user_id, title, status, category_id]):
        return jsonify({"error": "Missing essential item details."}), 400

    cursor = db.conn.cursor()
    try:
        query = """
            INSERT INTO Items (reported_by, category_id, title, description, status, image_url) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (user_id, category_id, title, description, status, image_url))
        db.conn.commit()
        return jsonify({"message": "Item reported successfully!", "id": cursor.lastrowid}), 201
    except mysql.connector.Error as err:
        return jsonify({"error": f"Could not submit report. {err}"}), 500
    finally:
        cursor.close()

@item_bp.route('', methods=['GET'])
def get_all_items():
    status_filter = request.args.get('status')
    
    cursor = db.conn.cursor(dictionary=True)
    
    base_query = """
        SELECT i.*, u.name AS reporter_name, c.name AS category_name
        FROM Items i
        JOIN Users u ON i.reported_by = u.user_id
        JOIN Categories c ON i.category_id = c.category_id
        WHERE i.status IN ('lost', 'found') 
    """
    
    params = []
    if status_filter in ['lost', 'found']:
        base_query += " AND i.status = %s"
        params.append(status_filter)

    cursor.execute(base_query, tuple(params))
    items = cursor.fetchall()
    cursor.close()
    
    return jsonify(items), 200