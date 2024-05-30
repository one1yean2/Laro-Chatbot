import json
from flask import Blueprint, request, jsonify
import pandas as pd

from src.views.custom_payload_format.format import custompayload, format_cart
from .. import redis_cache
from ..models import Order, db, User, Cart, CartDetail, Game

bp = Blueprint('cart', __name__, url_prefix='/cart')

@bp.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    # data = request.json
    data = request.data 
    json_data = json.loads(data)
    customer_id = json_data['customer_id']
    game_id = json_data['game_id']
    # print(customer_id,game_id)
    # Check if the user exists
    user = User.query.get(customer_id)
    print(user)
    if not user:
        add_user(customer_id)
        # return jsonify({'message': 'User not found'}), 404

    # Check if the game exists
    # TODO : VALIDATE GAME ID
    try:
        game_id = game_id.split(" ")[1]
        # print("Game id",game_id)
    except:
        #TODO : RETURN FLEX MESSAGE ERRROR
        return jsonify({'message': 'Wrong Format'}), 404
    
    game = Game.query.get(game_id)
    if not game:
        #TODO : RETURN FLEX MESSAGE ERRROR
        return jsonify({'message': 'Game not found'}), 404

    # Check if the user already has a cart
    cart = Cart.query.filter_by(customer_id=customer_id).first()
    if not cart:
        cart = Cart(customer_id=customer_id)
        db.session.add(cart)
        db.session.commit()

    # Add the game to the cart
    cart_detail = CartDetail(
        cart_id=cart.cart_id,
        game_id=game_id,
        game_quantity=1
    )
    db.session.add(cart_detail)
    db.session.commit()

    return jsonify({'message': 'Item added to cart successfully'}), 200

def add_user(customer_id):
    
    # customer_id = request.args.get('customer_id')
    # email = data.get('email')

    user = User(customer_id=customer_id)
    db.session.add(user)
    db.session.commit()



@bp.route('/view_cart', methods=['GET'])    
def view_cart():
    customer_id = request.args.get('customer_id')
    
    # TODO : VALIDATE CUSTOMER ID
    cart = pd.read_sql_query('SELECT cartdetail.game_id, cartdetail.game_quantity , game.price , game.game_name FROM cart INNER JOIN cartdetail ON cart.cart_id = cartdetail.cart_id INNER JOIN game ON cartdetail.game_id = game.game_id WHERE customer_id = "'+customer_id+'"',db.engine)
    if cart.empty:
        return jsonify({'message': 'Cart not found'}), 404
    print(cart)
    detail = cart.to_dict(orient='records')
    cp = format_cart(detail)
    out = custompayload(cp)
    return jsonify(out) , 200

        
        
@bp.route('/check_pending', methods=['GET'])
def check_pending():
    customer_id = request.args.get('customer_id')
    
    # TODO : VALIDATE CUSTOMER ID    
    
    
    order = Order.query.filter_by(user_id=customer_id, order_status='Pending').first()
    if order:
        return jsonify({'message': 'User already has an order in progress'}), 400
    else:
        return jsonify({'message': 'User does not have an order in progress'}), 200

@bp.route('/clear_cart', methods=['POST'])  
def clear_cart():
    customer_id = request.args.get('customer_id')
    cart = Cart.query.filter_by(customer_id=customer_id).first()
    if not cart:
        return jsonify({'message': 'Cart not found'}), 404
    db.session.delete(cart)
    db.session.commit()
    return jsonify({'message': 'Cart cleared successfully'}), 200