from flask import Flask 
from flask_redis import FlaskRedis
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_mail import Mail
from flask_openid import OpenID
from .config import Config
from .scheduler import create_jobs,scheduler
class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
redis_cache = FlaskRedis()
mail = Mail()
oid = OpenID()
# scheduler = APScheduler()

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)
    #init extension
    db.init_app(app)
    redis_cache.init_app(app)
    mail.init_app(app)
    oid.init_app(app)
    # create db table
    from . import models as _
    with app.app_context():
        db.create_all()
    
    # register blueprint
    from .views import cart , game , order , promotion_test ,steam_login
    app.register_blueprint(cart.bp)
    app.register_blueprint(game.bp)
    app.register_blueprint(order.bp)
    app.register_blueprint(promotion_test.bp)
    app.register_blueprint(steam_login.bp)
    
    scheduler.init_app(app)
    scheduler.start()
    create_jobs(app)
    
    for route in app.url_map.iter_rules():
        print(f"{route.methods} {route}")
    
    return app 