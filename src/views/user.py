import json
from flask import Blueprint
from sqlalchemy import update

from src.producer import noti_produce

from ..encrypt import decrypt_data, encrypt_data
from ..models import User
from ..views.custom_payload_format.format import error_payload_format, success_payload_format
from ..models import db
from flask import  request
bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/edit_profile', methods=['POST'])
def edit_profile():
    json_data = json.loads(request.data)
    customer_id = json_data['customer_id']
    noti_produce(customer_id)
    email = json_data['email']
    
    old_user = User.query.get(customer_id)
    
    encrypted_email = encrypt_data(email)
    
    if not old_user:
        new_user = User(customer_id=customer_id, email=encrypted_email)
        db.session.add(new_user)
        db.session.commit()
    else:
        old_user.email = encrypted_email
        db.session.commit()
    return success_payload_format('อัพเดท email',decrypt_data(old_user.email)) , 200

@bp.route('/get_info', methods=['GET'])
def get_info():
    customer_id = request.args.get('customer_id')
    noti_produce(customer_id)
    user = User.query.get(customer_id)
    
    if not user:
        return error_payload_format("ไม่พบข้อมูลผู้ใช้"), 200
    if user.email is None:
        return error_payload_format("ไม่พบอีเมลโปรดกรอกอีเมลของท่าน"), 200
    return success_payload_format('Email',decrypt_data(user.email)) , 200
    
    