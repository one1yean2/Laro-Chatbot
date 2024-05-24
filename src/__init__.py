from flask import Flask 
from flask_redis import FlaskRedis
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_mail import Mail
from .config import Config


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
redis_cache = FlaskRedis()
mail = Mail()



def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)
    #init extension
    db.init_app(app)
    redis_cache.init_app(app)
    mail.init_app(app)
    # create db table
    from . import models as _
    with app.app_context():
        db.create_all()
    
    # register blueprint
    from .views import cart , steamApi , game
    app.register_blueprint(cart.bp)
    app.register_blueprint(steamApi.bp)
    app.register_blueprint(game.bp)
    
    for route in app.url_map.iter_rules():
        print(f"{route.methods} {route}")
    
    return app 