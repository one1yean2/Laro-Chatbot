import json
from flask import Blueprint, request, jsonify
import pandas as pd
import requests
from ..models import db, User, Cart, CartDetail, Order, OrderItem , Promotion
from datetime import datetime, timedelta

bp = Blueprint('promotion', __name__, url_prefix='/promotion')

@bp.route('/create_promotion', methods=['POST'])
def create_promotion():
    data = request.data
    json_data = json.loads(data)
    print(json_data)
    #Create Promotion
    promotion = Promotion(
        promotion_id = json_data['promotion_id'],
        discount_type = json_data['discount_type'],
        discount_value = json_data['discount_value'],
        min_purchase = json_data['min_purchase'],
        start_date = datetime.now(),
        end_date = datetime.now() + timedelta(days=7),
        usage_limit = json_data['usage_limit'],
    )
    db.session.add(promotion)
    db.session.commit()
    
    return jsonify({'message': 'success'}) , 200

@bp.route('/get_promotion', methods=['GET'])
def get_promotion():
    promotion = Promotion.query.all()
    x = promotion.to_dict(orient='records')
    return jsonify(x)