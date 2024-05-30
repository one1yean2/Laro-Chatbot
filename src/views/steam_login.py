from flask import Blueprint

from src.models import User
STEAM_OPENID_URL = 'https://steamcommunity.com/openid'
from .. import oid
from ..models import db
from flask import Flask, session, redirect, url_for , request , current_app
bp = Blueprint('steam', __name__, url_prefix='/steam')
@bp.route('/')
def index():
    return 'Welcome to the Steam login example! <a href="steam.login">Login with Steam</a>'

@bp.route('/login')
@oid.loginhandler
def login():
    customer_id = request.args.get('customer_id')
    
    # user = User.query.filter_by(customer_id=customer_id).first()
    if customer_id:
        session['customer_id'] = customer_id
    for key, value in session.items():
        print(key, value)
    
    if 'steam_id' in session:
        print('test')
        return redirect(url_for('steam.profile'))

    return oid.try_login(STEAM_OPENID_URL, ask_for=['nickname'])

@oid.after_login
def create_or_login(resp):
    steam_id = resp.identity_url.split('/')[-1]
    session['steam_id'] = steam_id
    
    # user = User.query.filter_by(steam_id=steam_id).first()
    # if user is None:
    #     user = User(steam_id=steam_id)
    #     db.session.add(user)
    #     db.session.commit()
    customer_id = session.pop('customer_id', None)  # Retrieve and remove customer_id from session
    
    user = User.query.filter_by(steam_id=steam_id).first()
    if user is None:
        user = User(steam_id=steam_id, customer_id=customer_id)
        db.session.add(user)
        db.session.commit()
    
    return redirect(url_for('steam.profile'))

@bp.route('/profile')
def profile():
    if 'steam_id' not in session:
        return redirect(url_for('steam.login'))

    user = User.query.filter_by(steam_id=session['steam_id']).first()
    return f'Logged in as: {user.steam_id} <a href="logout">Logout</a>'

@bp.route('/logout')
def logout():
    session.pop('steam_id', None)
    for key, value in session.items():
        print(key, value)
    # print(session['steam_id'])
    #delete steam id in database
    
    return redirect(url_for('steam.index'))


