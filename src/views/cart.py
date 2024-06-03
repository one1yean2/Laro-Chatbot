import json
from flask import Blueprint, request, jsonify
import pandas as pd

from src.views.custom_payload_format.format import custompayload, error_payload_format, format_cart, success_payload_format
from ..producer import noti_produce
from ..models import Order, Promotion, db, User, Cart, CartDetail, Game
from .. import redis_cache

bp = Blueprint('cart', __name__, url_prefix='/cart')

@bp.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    json_data = json.loads(request.data )
    customer_id = json_data['customer_id']
    noti_produce(customer_id)
    game_id = json_data['game_id']
    
    # Check if the user exists
    user = User.query.get(customer_id)
    if not user:
        user = User(
            customer_id=customer_id
        )
        db.session.add(user)
        db.session.commit()
        
    # Check if the game exists
    game_id = game_id.split(" ")[1]

    game = Game.query.get(game_id)
    if not game:
        return error_payload_format("ไม่พบเกม"), 200

    # Check if the user already has a cart
    cart = Cart.query.filter_by(customer_id=customer_id).first()
    if not cart:
        cart = Cart(customer_id=customer_id)
        db.session.add(cart)
        db.session.commit()

    # Add the game to the cart
    cartDetail = CartDetail.query.filter_by(cart_id=cart.cart_id, game_id=game_id).first()
    if cartDetail:
        cartDetail.game_quantity += 1
        db.session.commit()
        return jsonify({'message': 'Item quantity updated successfully'}), 200
    else :
        cart_detail = CartDetail(
            cart_id=cart.cart_id,
            game_id=game_id,
            game_quantity=1
        )
        db.session.add(cart_detail)
        db.session.commit()
        
    return jsonify({'message': 'Item added to cart successfully'}), 200





@bp.route('/view_cart', methods=['GET'])    
def view_cart():
    customer_id = request.args.get('customer_id')
    noti_produce(customer_id)
    # TODO : VALIDATE CUSTOMER ID
    cart = pd.read_sql_query('SELECT cartdetail.game_id, cartdetail.game_quantity , game.price , game.game_name FROM cart INNER JOIN cartdetail ON cart.cart_id = cartdetail.cart_id INNER JOIN game ON cartdetail.game_id = game.game_id WHERE customer_id = "'+customer_id+'"',db.engine)

    if cart.empty:
        return error_payload_format("ไม่มีรายการในรถเข็น") , 200

    used_promo = redis_cache.get("promotion_id"+customer_id)
    pro = Promotion.query.get(used_promo)


    detail = cart.to_dict(orient='records')
    total_price = sum(clean_price(item['price']) * int(item['game_quantity']) for item in detail)
    if pro is not None:
        if pro.discount_type == "literal":
            discount_value = pro.discount_value
        else:
            discount_value = (total_price*pro.discount_value)/100
        if total_price < pro.min_purchase:
            discount_value = 0
    else:
        discount_value = 0
    cp = format_cart(detail,promotion=discount_value)
    out = custompayload(cp)
    return jsonify(out) , 200

def clean_price(price):
    # Remove the currency symbol and commas
    return float(price.replace(',', '').replace('฿', '').strip())
        

def check_pending():
    customer_id = request.args.get('customer_id')

    order = Order.query.filter_by(user_id=customer_id, order_status='Pending').first()
    if order:
        return jsonify({'message': 'User already has an order in progress'}), 400
    else:
        return jsonify({'message': 'User does not have an order in progress'}), 200

@bp.route('/clear_cart', methods=['POST'])  
def clear_cart():
    json_data = json.loads(request.data)
    customer_id = json_data['customer_id']
    noti_produce(customer_id)
    cart = Cart.query.filter_by(customer_id=customer_id).first()
    if not cart:
        return error_payload_format("ไม่มีรายการในรถเข็น"),200
    cart_detail = CartDetail.query.filter_by(cart_id=cart.cart_id).all()
    for detail in cart_detail:
        db.session.delete(detail)
    db.session.delete(cart)
    db.session.commit()
    return success_payload_format("รถเข็น","เคลียร์รายการเรียบร้อย"), 200