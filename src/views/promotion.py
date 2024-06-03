import json
from flask import Blueprint, request, jsonify
import pandas as pd
from datetime import datetime, timedelta

from src.producer import noti_produce

from .custom_payload_format.format import  custompayload, error_payload_format, promotion_payload_format, success_payload_format
from ..models import Order, User, db,Promotion
from .. import redis_cache

bp = Blueprint('promotion', __name__, url_prefix='/promotion')

@bp.route('/create_promotion', methods=['POST'])
def create_promotion():
    
    json_data = json.loads(request.data)

    #Create Promotion
    promotion = Promotion(
        promotion_name = json_data['promotion_name'],
        discount_type = json_data['discount_type'],
        discount_value = json_data['discount_value'],
        min_purchase = json_data['min_purchase'],
        start_date = datetime.now(),
        end_date = datetime.now() + timedelta(days=json_data['time_limit']),
        usage_limit = json_data['usage_limit'],
    )
    db.session.add(promotion)
    db.session.commit()
    
    return jsonify({'message': 'success'}) , 200

@bp.route('/get_promotion', methods=['GET'])
def get_promotion():
    customer_id = request.args.get('customer_id')
    noti_produce(customer_id)
    promotion = pd.read_sql_query('SELECT * FROM promotion',db.engine)

    if promotion.empty:
        return error_payload_format("ณ ขณะนี้ไม่มีโปรโมชั่น") , 200
    user = User.query.get(customer_id)
    if not user:
        return error_payload_format("ไม่พบข้อมูลผู้ใช้") , 200
    promotions = promotion.to_dict(orient='records')
    list = []
    for promo in promotions:
        orders = Order.query.filter_by(user_id=customer_id, promotion_id=promo['promotion_id']).all()
        if len(orders) >= promo['usage_limit']:
            continue
        list.append(promotion_payload_format(promo))
    carousel = {
        "type" : "carousel",
        "contents" : list[:10]
    }
    out = custompayload(carousel)
    return jsonify(out),200

@bp.route('/use_promotion', methods=['POST'])
def use_promotion():
    json_data = json.loads(request.data)
    
    promotion_id = json_data['promotion_id'].split(" ")[1]
    customer_id = json_data['customer_id']
    noti_produce(customer_id)
    redis_cache.setex("promotion_id"+json_data['customer_id'], 3600,str(promotion_id))
    return success_payload_format("ใช้โปรโมชั่น","ดำเนินการซื้อได้เลยครับ") , 200

@bp.route('/discard_promotion', methods=['GET'])
def discard_promotion():
    customer_id = request.args.get('customer_id')
    noti_produce(customer_id)
    user = User.query.get(customer_id)
    if not user:
        return error_payload_format("ไม่พบข้อมูลผู้ใช้") , 200
    redis_cache.delete("promotion_id"+customer_id)
    
    return success_payload_format("โปรโมชั่น","ยกเลิกโปรโมชั่น") , 200