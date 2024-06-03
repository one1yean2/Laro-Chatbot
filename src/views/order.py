import json
import threading
import uuid
from flask import Blueprint, current_app, request, jsonify
import pandas as pd
import requests
from sqlalchemy import update
from flask_mail import Message

from src.encrypt import decrypt_data
from src.producer import noti_produce
from .. import redis_cache,mail
from src.views.custom_payload_format.format import custompayload, error_payload_format, format_cart, his_order_payload_format, order_payload_format, success_payload_format
from ..models import Promotion, User, db, Cart, CartDetail, Order, OrderItem
from datetime import datetime

bp = Blueprint('order', __name__, url_prefix='/order')

@bp.route('/create_order', methods=['POST'])
def create_order():
    
    json_data = json.loads(request.data)
    customer_id = json_data['customer_id']
    user = User.query.get(customer_id)
    noti_produce(customer_id)
    if user.email is None:
        return error_payload_format("กรุณากรอกอีเมลของคุณ ในข้อมูลส่วนตัว"), 200
    pending = Order.query.filter_by(user_id=customer_id,order_status='Pending').first()
    if pending:
        return error_payload_format("โปรดชำระเงินคําสั่งซื้อก่อนหน้านี้"), 200
    
    promotion_id  = redis_cache.getdel("promotion_id"+customer_id)
    if promotion_id is None:
        promotion_id = None
    else:
        promotion = Promotion.query.filter_by(promotion_id=promotion_id).first()
        if not promotion:
            return error_payload_format("ไม่พบโปรโมชั่น"), 200
        
        orders = Order.query.filter_by(user_id=customer_id,promotion_id=promotion_id)

        if orders.count() >= promotion.usage_limit:
            return error_payload_format("ใช้โปรจนครบจำนวนครั้งแล้ว"), 200
    
    # Retrieve the user's cart
    cart = Cart.query.filter_by(customer_id=customer_id).first()
    if not cart or not cart.items:
        return error_payload_format("ไม่พบรถเข็น"), 200

    # Calculate total cost

    total_cost = sum(clean_price(item.game.price) * item.game_quantity for item in cart.items)
    if promotion_id is not None:
        if promotion.min_purchase <= total_cost:
            if promotion.discount_type == 'literal':
                total_cost = total_cost - promotion.discount_value
            else :
                total_cost = total_cost - (total_cost * (promotion.discount_value/100))
        else:
            return error_payload_format("ยอดรวมไม่ถึงราคาขั้นต่ำ"), 200
    # Create a new order
    new_order = Order(
        user_id=customer_id,
        order_status='Pending',
        order_date=datetime.now(),
        total_cost=total_cost,
        promotion_id=promotion_id
    )
    db.session.add(new_order)
    db.session.flush()  # Ensure new_order gets an ID before adding OrderItems

    # Move all cart items to the new order
    for cart_item in cart.items:
        order_item = OrderItem(
            order_id=new_order.order_id,
            game_id=cart_item.game_id,
            game_name=cart_item.game.game_name,
            game_quantity=cart_item.game_quantity,
            price_when_ordered=cart_item.game.price
        )
        db.session.add(order_item)
    # Clear Cart detail
    db.session.query(CartDetail).filter_by(cart_id=cart.cart_id).delete()
    # Clear the cart
    db.session.delete(cart)
    db.session.commit()

    return view_order(customer_id,promotion_id), 200
def clean_price(price):
    # Remove the currency symbol and commas
    return float(price.replace(',', '').replace('฿', '').strip())
    
# @bp.route('/view_order', methods=['GET'])
def view_order(customer_id,promotion_id):
    order = pd.read_sql_query('SELECT * FROM "order" INNER JOIN "orderitem" ON "order".order_id = "orderitem".order_id WHERE "order".user_id = "'+customer_id+'" AND "order".order_status = "Pending"',db.engine)
    pro=Promotion.query.filter_by(promotion_id=promotion_id)
    if order.empty:
        return error_payload_format("ไม่พบรายการ") , 200

    # used_promo = redis_cache.get("promotion_id"+customer_id)

    
    detail = order.to_dict(orient='records')
    total_cost = Order.query.filter_by(user_id=customer_id, order_status='Pending').first().total_cost
    pro = Promotion.query.get(promotion_id)
    if pro is not None:
        if pro.discount_type == "literal":
            discount_value = pro.discount_value
        else:
            discount_value = (total_cost*pro.discount_value)/100
        if total_cost < pro.min_purchase:
            discount_value = 0
    else:
        discount_value = 0
    cp = order_payload_format(detail,discount_value)
    out = custompayload(cp)
    return jsonify(out)

@bp.route('/cancel_order', methods=['POST'])
def cancel_order():
    data = request.data
    json_data = json.loads(data)
    order_id = json_data['order_id'].split(" ")[1]
    customer_id  = json_data['customer_id']
    noti_produce(customer_id)
    order = Order.query.filter_by(order_id=order_id,user_id=customer_id).first()
    if not order:
        return error_payload_format("Order not found"), 200
    db.session.delete(order)
    db.session.commit()
    # if not order:
    #     return custompayload(error_payload_format("Order not found")), 200
    # order.order_status = 'Cancelled'
    # db.session.commit()
    return error_payload_format("Order cancelled"), 200
@bp.route('/order_history', methods=['GET'])
def order_history():
    customer_id = request.args.get('customer_id')
    cart = pd.read_sql_query('SELECT * FROM "order" INNER JOIN "orderitem" ON "order".order_id = "orderitem".order_id WHERE "order".user_id = "'+customer_id+'"ORDER BY "order".order_id DESC',db.engine)
    noti_produce(customer_id)
    # cart = Cart.query.filter_by(customer_id=customer_id).first()/
    if cart.empty:
        return error_payload_format("ไม่มีรายการในรถเข็น") , 200
        # return jsonify({'message': 'Cart not found'}), 404
    # cartDetail = CartDetail.query.filter_by(cart_id=cart.cart_id).all()
    detail = cart.to_dict(orient='records')
    # print(detail)
    mylist = []
    for item in detail:
        # print(item['order_id'])
        total_cost = Order.query.filter_by(order_id=item['order_id']).first().total_cost
        promotion_id = Order.query.filter_by(order_id=item['order_id']).first().promotion_id
        pro = Promotion.query.get(promotion_id)
        if pro is not None:
            if pro.discount_type == "literal":
                discount_value = pro.discount_value
            else:
                discount_value = (total_cost*pro.discount_value)/100
            if total_cost < pro.min_purchase:
                discount_value = 0
        else:
            discount_value = 0
        if item['order_status'] == "Pending":
            mylist.append(order_payload_format([item],discount_value))
        else:
            mylist.append(his_order_payload_format([item],discount_value))
    # cp = 
    # customer_id = request.args.get('customer_id')
    # order = pd.read_sql_query('SELECT * FROM "order" INNER JOIN "orderitem" ON "order".order_id = "orderitem".order_id WHERE "order".user_id = "'+customer_id+'"',db.engine)
    # if order.empty:
    #     return custompayload(error_payload_format("ไม่มีประวัติการสั่งซื้อ")) , 200
    # order_history = order.to_dict(orient='records')
    # print(order_history)
    # mylist = []
    # for item in order_history:
        # print(item)
    # cp  = order_payload_format(order_history)
    carousel = {
        "type" : "carousel",
        "contents" : mylist[:10]
    }
    out = custompayload(carousel)
    return jsonify(out)
    # return 'eiei',200
        # item['order_date'] = item['order_date'].strftime('%Y-%m-%d %H:%M:%S')
        
@bp.route('/view_pending_order', methods=['GET'])
def view_pending_order():
    # TODO : VALIDATE CUSTOMER ID
    customer_id = request.args.get('customer_id')
    order = pd.read_sql_query('SELECT * FROM "order" INNER JOIN "orderitem" ON "order".order_id = "orderitem".order_id WHERE "order".user_id = "'+customer_id+'" AND "order".order_status = "Pending"',db.engine)
    noti_produce(customer_id)
    if order.empty:
        return error_payload_format("ไม่มีรายการที่ค้างอยู่") , 200

    detail = order.to_dict(orient='records')
    promotion_id = Order.query.filter_by(user_id=customer_id, order_status='Pending').first().promotion_id
    pro = Promotion.query.get(promotion_id)
    total_cost = Order.query.filter_by(user_id=customer_id, order_status='Pending').first().total_cost
    if pro is not None:
        if pro.discount_type == "literal":
            discount_value = pro.discount_value
        else:
            discount_value = (total_cost*pro.discount_value)/100
        if total_cost < pro.min_purchase:
            discount_value = 0
    else:
        discount_value = 0
    
    cp = order_payload_format(detail,discount_value)
    out = custompayload(cp)
    return jsonify(out)
        
        
        
@bp.route('/check_slip', methods=['POST'])
def check_slip():
    data = request.data
    json_data = json.loads(data)
    image = json_data['image']
    customer_id = json_data['customer_id']
    slipok = requests.post('https://api.slipok.com/api/line/apikey/22245',headers={'x-authorization':'SLIPOKEM77IPC'},json={'url':image})
    noti_produce(customer_id)
    data = slipok.json()

    if data['success'] == True:
        reciever = data['data']['receiver']
        if reciever['displayName'] == 'นาย วันหนึ่ง อ' and reciever['name'] == 'WONNEUNG Y' and reciever['proxy']['value'] == "xxx-xxx-1247":
            
            order = pd.read_sql_query('SELECT * FROM "order" INNER JOIN "orderitem" ON "order".order_id = "orderitem".order_id WHERE "order".user_id = "'+customer_id+'" AND "order".order_status = "Pending"',db.engine)
            order_paid = pd.read_sql_query('SELECT * FROM "order" INNER JOIN "orderitem" ON "order".order_id = "orderitem".order_id WHERE "order".user_id = "'+customer_id+'" AND "order".order_status = "Paid"',db.engine)
            if not order.empty:
                for item in order_paid.to_dict(orient='records'):
                    if item['qrcode_data'] == data['data']['qrcodeData']:
                        return error_payload_format("Slip นี้เคยถูกใช้แล้ว"), 200
                if order['total_cost'][0] == data['data']['paidLocalAmount']:
                    values = {
                        'order_status' : 'Paid',
                        'qrcode_data' : data['data']['qrcodeData']
                    }
                    db.session.execute(
                            update(Order).where(
                                Order.user_id == customer_id
                            ).values(values)
                    )
                    db.session.commit()
                    
                    user = User.query.filter_by(customer_id=customer_id).first()
                    #get user email
                    
                    app = current_app._get_current_object()
                    # print(orders)
                    threading.Thread(target=sending_key,args=(app,decrypt_data(user.email),order)).start()
                    
                    return success_payload_format("เรียบร้อย","จ่ายเงินสําเร็จ"), 200
                else:
                    return error_payload_format("จำนวนเงินไม่ถูกต้อง"), 200
            else:
                return error_payload_format("ไม่มีรายการที่ต้องชำระ"), 200
        else:
            return error_payload_format("สลิปไม่ถูกต้อง"), 200
    else:
        return error_payload_format("สลิปไม่ถูกต้อง"), 200
    
def sending_key(app,email,games):
    with app.app_context():
        msg_title = "[OTP-Yean]"
        sender = "noreply@gmail.com"
        msg = Message(msg_title, sender=sender,recipients=[email])
        msg.body = ''
        for game in games['game_name']:
            # print(game)
            msg.body += "Game : "+game+"\n"
            msg.body += "Key : "+gen_key_game()+"\n\n"
        mail.send(msg)
def gen_key_game():
    return str(uuid.uuid4())