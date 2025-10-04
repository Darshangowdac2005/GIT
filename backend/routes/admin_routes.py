# backend/routes/admin_routes.py

from flask import Blueprint, request, jsonify
from config.db_connector import db
from utils.security import admin_required
from utils.notification import send_claim_resolved_emails
from models.item_model import Item
from models.claim_model import Claim

admin_bp = Blueprint('admin_bp', __name__)

@admin_bp.route('/claims/pending', methods=['GET'])
@admin_required
def get_pending_claims():
    """Admin dashboard view: lists all pending claims."""
    cursor = db.conn.cursor(dictionary=True)
    
    # Complex query to fetch claim details along with item titles and user emails
    query = """
        SELECT 
            c.claim_id, c.claimed_at, c.verification_details,
            i.item_id, i.title AS item_title, i.status AS item_status, i.reported_by,
            u_claim.name AS claimant_name, u_claim.email AS claimant_email
        FROM Claims c
        JOIN Items i ON c.item_id = i.item_id
        JOIN Users u_claim ON c.claimant_id = u_claim.user_id
        WHERE c.claim_status = %s 
    """
    cursor.execute(query, (Claim.STATUSES['PENDING'],))
    claims = cursor.fetchall()
    cursor.close()
    return jsonify(claims)

@admin_bp.route('/claims/resolve', methods=['POST'])
@admin_required
def resolve_claim():
    """Admin action: approves a claim, marks the item as resolved, and sends emails."""
    admin_id = request.user_id
    data = request.json
    claim_id = data.get('claim_id')
    resolution_type = data.get('resolution_type') # 'approve' or 'reject'
    
    if not claim_id or resolution_type not in ['approve', 'reject']:
        return jsonify({"error": "Missing claim ID or invalid resolution type."}), 400

    cursor = db.conn.cursor(dictionary=True)
    
    try:
        if resolution_type == 'approve':
            # 1. Update Claim Status to APPROVED
            cursor.execute("UPDATE Claims SET claim_status = %s WHERE claim_id = %s", 
                           (Claim.STATUSES['APPROVED'], claim_id))
            
            # 2. Update Item Status to RESOLVED (Crucial for the video's resolved status)
            cursor.execute("SELECT item_id, claimant_id FROM Claims WHERE claim_id = %s", (claim_id,))
            claim_info = cursor.fetchone()
            item_id = claim_info['item_id']
            claimant_id = claim_info['claimant_id']

            cursor.execute("UPDATE Items SET status = %s WHERE item_id = %s", 
                           (Item.STATUSES['RESOLVED'], item_id))
            
            # 3. Fetch item reporter and send notification emails (utility function)
            send_claim_resolved_emails(item_id, claimant_id, admin_id) 
            
            db.conn.commit()
            return jsonify({"message": "Claim approved and resolved successfully. Notifications sent."}), 200

        elif resolution_type == 'reject':
            cursor.execute("UPDATE Claims SET claim_status = %s WHERE claim_id = %s", 
                           (Claim.STATUSES['REJECTED'], claim_id))
            db.conn.commit()
            return jsonify({"message": "Claim rejected."}), 200

    except mysql.connector.Error as err:
        db.conn.rollback()
        return jsonify({"error": f"Database error during resolution: {err}"}), 500
    finally:
        cursor.close()