import json
from flask import Blueprint, request, jsonify
import pandas as pd
import requests
from ..models import Promotion, db, User, Cart, CartDetail, Order, OrderItem
from datetime import datetime

bp = Blueprint('order', __name__, url_prefix='/order')

@bp.route('/create_order', methods=['POST'])
def checkout():
    # customer_id = request..get('customer_id')
    data = request.data
    json_data = json.loads(data)
    #access to customer_id from body
    
    
    customer_id = json_data['customer_id']
    # TODO : IMPLEMENT PROMOTION
    promotion_id = json_data['promotion_id']
    
    # query = f'SELECT promotion_id FROM promotion WHERE promotion_id LIKE "%{promotion_id}%"'
    promotion = Promotion.query.filter_by(promotion_id=promotion_id).first()
    if not promotion:
        return jsonify({'message': 'Promotion not found'}), 404
    
    orders = Order.query.filter_by(customer_id=customer_id,promotion_id=promotion_id)
    
    if orders.count() < promotion.usage_limit:
        return jsonify({'message': 'User reach the usage limit'}), 400
    
    # Retrieve the user's cart
    cart = Cart.query.filter_by(customer_id=customer_id).first()
    if not cart or not cart.items:
        return jsonify({'message': 'Cart is empty or not found'}), 404

    # Calculate total cost
    def clean_price(price):
        # Remove the currency symbol and commas
        return float(price.replace(',', '').replace('฿', '').strip())
    
    total_cost = sum(clean_price(item.game.price) * item.game_quantity for item in cart.items)

    # Create a new order
    new_order = Order(
        user_id=customer_id,
        order_status='Pending',
        order_date=datetime.now(),
        total_cost=total_cost
    )
    db.session.add(new_order)
    db.session.flush()  # Ensure new_order gets an ID before adding OrderItems

    # Move all cart items to the new order
    for cart_item in cart.items:
        order_item = OrderItem(
            order_id=new_order.order_id,
            game_id=cart_item.game_id,
            game_name = cart_item.game_name,
            game_quantity=cart_item.game_quantity,
            price_when_ordered=cart_item.game.price
        )
        db.session.add(order_item)
    # Clear Cart detail
    db.session.query(CartDetail).filter_by(cart_id=cart.cart_id).delete()
    # Clear the cart
    db.session.delete(cart)
    db.session.commit()

    return jsonify({'message': 'Order created successfully', 'order_id': new_order.order_id}), 200

# @bp.route('/view_order', methods=['GET'])
# def view_order():
#     customer_id = request.args.get('customer_id')
    
#     orders = Order.query.filter_by(customer_id=customer_id).all()
    
#     # TODO : VALIDATE CUSTOMER ID
    
#     # df = pd.read_sql_query('SELECT cartdetail.game_id, cartdetail.game_quantity , game.price , game.game_name FROM cart INNER JOIN cartdetail ON cart.cart_id = cartdetail.cart_id INNER JOIN game ON cartdetail.game_id = game.game_id WHERE customer_id = "'+customer_id+'"',db.engine)
#     # df = pd.read_sql_query('SELECT  WHERE customer_id = "'+customer_id+'"',db.engine)
    
#     print(df)
#     detail = df.to_dict(orient='records')
#     loop_through_order(detail)
#     return jsonify(df.to_dict()) , 200

def loop_through_order(detail):
    for item in detail:
        print(item)
@bp.route('/check_slip', methods=['POST'])
def check_slip():
    data = request.data
    json_data = json.loads(data)
    image = json_data['image']
    slipok = requests.post('https://api.slipok.com/api/line/apikey/22245',headers={'x-authorization':'SLIPOKEM77IPC'},json={'url':image})
    # TODO : IMPLEMENT SLIPOK API TO CHECK AND VALIDATE IMAGE AND CHECK TOTAL MONEY, FOR NOW JUST RETURN SUCCESS 
    
    # TODO : QRCODE DATA INTO DATABASE FOR CHECK IF ALREADY USE OR NOT,
    
    data = slipok.json()
    # print(slipok.json())
    # TODO: VALIDATE TOTAL MONEY
    
    # print(image)
    return slipok.json() , 200