from sqlalchemy import Column, Integer, String
from . import db


class User(db.Model):      
    __tablename__ = "user"

    id = Column(
        Integer,
        index=True,
        nullable=False,
        primary_key=True
    )
    
    userlineid = Column(String)
    email = Column(String)

class Promotion(db.Model):
    __tablename__ = "promotion"
    
    id = Column(
        Integer,
        index=True,
        nullable=False,
        primary_key=True
    )
    
    promotionName = Column(String)
    time = Column(String)
class Game(db.Model):
    __tablename__ = 'games'
    
    appid = Column(Integer, primary_key=True)
    name = Column(String)
    developer = Column(String)
    publisher = Column(String)
    positive = Column(Integer)
    negative = Column(Integer)
    price = Column(Integer)
    initialprice = Column(Integer)
    discount = Column(Integer)
    genre = Column(String)
    languages = Column(String)
    
    
    is_free = Column(Integer)
    detailed_description = Column(String)
    about_the_game = Column(String)
    short_description = Column(String)
    header_image = Column(String)
    website = Column(String)
    discount_percent = Column(Integer)
    final_formatted = Column(String)
    
class Order(db.Model):
    __tablename__ = "order"

    id = Column(
        Integer,
        index=True,
        nullable=False,
        primary_key=True
    )

    user_id = Column(Integer)
    game_id = Column(Integer)