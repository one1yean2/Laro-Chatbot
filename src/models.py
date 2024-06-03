
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Boolean, func
from sqlalchemy.orm import relationship
from . import db

class GameList(db.Model):
    __tablename__ = "gamelist"
    id = Column(Integer, index=True, nullable=False, primary_key=True)
    game_id = Column(String)
    game_name = Column(String, nullable=False)


class Order(db.Model):
    __tablename__ = "order"

    order_id = Column(Integer, index=True, nullable=False, primary_key=True)
    user_id = Column(String, ForeignKey('user.customer_id'))
    order_status = Column(String)
    order_date = Column(DateTime(timezone=True),nullable=False)
    total_cost = Column(Integer)
    promotion_id = Column(String, ForeignKey('promotion.promotion_id'))
    qrcode_data = Column(String)
    
    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")

    promotion = relationship("Promotion", back_populates="orders")


class OrderItem(db.Model):
    __tablename__ = "orderitem"

    order_item_id = Column(Integer, index=True, nullable=False, primary_key=True)
    order_id = Column(Integer, ForeignKey('order.order_id'))
    # game_id = Column(String, ForeignKey('game.game_id'))
    game_id = Column(String)
    game_name = Column(String)
    game_quantity = Column(String)
    price_when_ordered = Column(String)
    
    order = relationship("Order", back_populates="items")
    # game = relationship("Game", back_populates="orders")


class User(db.Model):      
    __tablename__ = "user"

    customer_id = Column(String, index=True, nullable=False, primary_key=True)
    email = Column(String)
    steam_id = Column(String)
    
    carts = relationship("Cart", back_populates="user")
    orders = relationship("Order", back_populates="user")


class Cart(db.Model):
    __tablename__ = "cart"

    cart_id = Column(Integer, index=True, nullable=False, primary_key=True)
    customer_id = Column(String, ForeignKey('user.customer_id'))
    
    user = relationship("User", back_populates="carts")
    items = relationship("CartDetail", back_populates="cart")


class CartDetail(db.Model):
    __tablename__ = "cartdetail"

    cartdetail_id = Column(Integer, index=True, nullable=False, primary_key=True)
    cart_id = Column(Integer, ForeignKey('cart.cart_id'))
    game_id = Column(String, ForeignKey('game.game_id'))
    game_quantity = Column(Integer)
    
    cart = relationship("Cart", back_populates="items")
    game = relationship("Game", back_populates="carts")


class Game(db.Model):
    __tablename__ = 'game'
    game_id = Column(String, index=True, primary_key=True)
    game_name = Column(String)
    
    is_free = Column(Boolean)
    short_description = Column(String)
    image = Column(String)
    discount_percent = Column(Integer)
    price = Column(String)
    genres = Column(String)
    developer = Column(String)
    review_positive = Column(Integer)
    review_negative = Column(Integer)
    
    carts = relationship("CartDetail", back_populates="game")
    # orders = relationship("OrderItem", back_populates="game")

class Promotion(db.Model):
    __tablename__ = 'promotion'
    
    promotion_id = Column(Integer, index=True, primary_key=True)
    promotion_name  = Column(String)
    discount_type = Column(db.String(20),nullable=False)
    discount_value = Column(db.Float,nullable=True)
    min_purchase = Column(db.Float,nullable=True)
    start_date = Column(DateTime(timezone=True),nullable=False)
    end_date = Column(DateTime(timezone=True),nullable=False)
    usage_limit = Column(Integer,nullable=True)
    
    orders = relationship("Order", back_populates="promotion")
    # orders = relationship("OrderItem", back_populates="promotion")