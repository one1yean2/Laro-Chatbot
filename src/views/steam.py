from flask import Blueprint
import requests
from sqlalchemy import update

from src.encrypt import encrypt_data
from src.models import User
from src.producer import noti_produce
from src.views.custom_payload_format.format import error_payload_format, success_payload_format
from .. import oid , redis_cache
from ..models import GameList, db
from flask import session, request 
bp = Blueprint('steam', __name__, url_prefix='/steam')

STEAM_OPENID_URL = 'https://steamcommunity.com/openid'

@bp.route('/login')
@oid.loginhandler
def login():
    customer_id = request.args.get('customer_id')
    noti_produce(customer_id)
    if customer_id:
        session['customer_id'] = customer_id
    # for key, value in session.items():
    #     print(key, value)


    return oid.try_login(STEAM_OPENID_URL, ask_for=['nickname'])

@oid.after_login
def create_or_login(resp):
    steam_id = resp.identity_url.split('/')[-1]
    session['steam_id'] = steam_id
    redis_cache.set("steam_id"+str(session['customer_id']), steam_id)
    customer_id = session.pop('customer_id', None) 
    encrypted_steam_id = encrypt_data(steam_id)
    user = User.query.filter_by(customer_id=customer_id).first()
    if user is None:
        user = User(steam_id=encrypted_steam_id, customer_id=customer_id)
        db.session.add(user)
        db.session.commit()
    else:
        
        values = {
            'steam_id': encrypted_steam_id
        }
        db.session.execute(
                update(User).where(
                    User.customer_id == customer_id
                ).values(values)
            )
        db.session.commit()
    LINE_ACCESS_TOKEN = "2FiR3KE3mT5uHuaSkv7GDqB+Vxgq4QEYK7vG6aLpfyY91cCwDTGiKl7vKBJMUhVvzx5QUCjP1OHV7aVQVe4rQ9jPLHNtShWyIhSqsroEVxVBqXGhdgSA6D5Or3kUwvejEQc1VqIhgxTfhWlHLKrxRQdB04t89/1O/w1cDnyilFU="
    # user_id = ""

    LINE_API_URL = "https://api.line.me/v2/bot/message/push"




    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + LINE_ACCESS_TOKEN,
    }
    payload = {
        "to": customer_id,
        "messages": [
            {
                "type": "text",
                "text": "เข้าสู่ระบบ Steam เรียบร้อยครับ"
            }
        ]
    }

    print("Sending message to user:", customer_id)
    response = requests.post(LINE_API_URL, headers=headers, json=payload)
    print("Message sent. Response Status Code:", response.status_code)
    return f'เข้าสู่ระบบเรียบร้อยครับ'


@bp.route('/logout', methods=['GET'])
def logout():
    customer_id = request.args.get('customer_id')
    noti_produce(customer_id)
    sid = redis_cache.get("steam_id"+customer_id)
    if sid:
        redis_cache.delete("steam_id"+customer_id)
    # session.pop('steam_id', None)
    else :
        return error_payload_format("ไม่ได้ Login ไว้"), 200
        
    
    return success_payload_format("สำเร็จ","ออกจากระบบ Steam") , 200

@bp.route('/get_info', methods=['GET'])
def get_info():
    customer_id = request.args.get('customer_id')
    noti_produce(customer_id)
    sid = redis_cache.get("steam_id"+str(customer_id))
    if sid:
        STEAM_URL ="https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=ECF5EA6F18F37B8600102FE342FA06AD&steamid=+"+sid+"&format=json"
        resp = requests.get(STEAM_URL)
        json_data = resp.json()
        txt = "คุณมีเกมทั้งหมด "+str(json_data['response']['game_count'])+" เกม\n"
        for game in json_data['response']['games']:
            gameq = GameList.query.filter_by(game_id=game['appid']).first()
            if not gameq:
                continue
            txt += gameq.game_name +" : "+str(game['playtime_forever'])+" นาที\n"
        return success_payload_format('Steam',txt) , 200
        
    return "Logged out" , 200
