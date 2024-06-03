from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from redis import Redis
from flask_mail import Mail
from flask_openid import OpenID





from .config import Config
from .scheduler import create_jobs,scheduler
class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

mail = Mail()
oid = OpenID()
redis_cache = Redis(host="localhost",port=6379, decode_responses=True)
# scheduler = APScheduler()

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)
    #init extension
    db.init_app(app)
    mail.init_app(app)
    oid.init_app(app)
    # redis_cache.init_app(app)
    # create db table
    from . import models as _
    with app.app_context():
        db.create_all()
    
    # register blueprint
    from .views import cart , game , order , promotion , user , steam
    app.register_blueprint(cart.bp)
    app.register_blueprint(game.bp)
    app.register_blueprint(order.bp)
    app.register_blueprint(promotion.bp)
    app.register_blueprint(steam.bp)
    app.register_blueprint(user.bp)
    
    scheduler.init_app(app)
    scheduler.start()
    create_jobs(app)
    
    for route in app.url_map.iter_rules():
        print(f"{route.methods} {route}")
    
    return app 