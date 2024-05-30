import redis
import datetime
from sqlalchemy.orm import sessionmaker
from ..models import Promotion , db

# Redis configuration
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

# SQLAlchemy session setup
Session = sessionmaker(bind=db.engine)
session = Session()

# Add promotion to Redis
def add_promotion_to_redis(promotion):
    promotion_key = f"promotion:{promotion.promotion_id}"
    redis_client.hmset(promotion_key, {
        "name": promotion.name,
        "discount_percent": promotion.discount_percent,
        "start_date": promotion.start_date.isoformat(),
        "end_date": promotion.end_date.isoformat()
    })
    redis_client.zadd("promotions", {promotion_key: promotion.end_date.timestamp()})

# Add flash promotion to Redis
def add_flash_promotion_to_redis(flash_promotion):
    flash_promotion_key = f"flash_promotion:{flash_promotion.flash_promotion_id}"
    redis_client.hmset(flash_promotion_key, {
        "name": flash_promotion.name,
        "discount_percent": flash_promotion.discount_percent,
        "start_date": flash_promotion.start_date.isoformat(),
        "end_date": flash_promotion.end_date.isoformat()
    })
    redis_client.zadd("flash_promotions", {flash_promotion_key: flash_promotion.end_date.timestamp()})

# Retrieve active promotions from Redis
def get_active_promotions():
    current_time = datetime.datetime.now().timestamp()
    promotion_keys = redis_client.zrangebyscore("promotions", current_time, '+inf')
    promotions = [redis_client.hgetall(key) for key in promotion_keys]
    return promotions

# Retrieve active flash promotions from Redis
def get_active_flash_promotions():
    current_time = datetime.datetime.now().timestamp()
    flash_promotion_keys = redis_client.zrangebyscore("flash_promotions", current_time, '+inf')
    flash_promotions = [redis_client.hgetall(key) for key in flash_promotion_keys]
    return flash_promotions

# Clean expired promotions from Redis
def clean_expired_promotions():
    current_time = datetime.datetime.now().timestamp()
    expired_keys = redis_client.zrangebyscore("promotions", '-inf', current_time)
    for key in expired_keys:
        redis_client.delete(key)
        redis_client.zrem("promotions", key)

# Clean expired flash promotions from Redis
def clean_expired_flash_promotions():
    current_time = datetime.datetime.now().timestamp()
    expired_keys = redis_client.zrangebyscore("flash_promotions", '-inf', current_time)
    for key in expired_keys:
        redis_client.delete(key)
        redis_client.zrem("flash_promotions", key)

# Example: Add promotion and flash promotion to Redis
def add_example_promotions():
    promotion = session.query(Promotion).first()  # Assuming you have promotions in your DB
    flash_promotion = session.query(FlashPromotion).first()  # Assuming you have flash promotions in your DB
    if promotion:
        add_promotion_to_redis(promotion)
    if flash_promotion:
        add_flash_promotion_to_redis(flash_promotion)

# Example: Fetch active promotions
def print_active_promotions():
    promotions = get_active_promotions()
    flash_promotions = get_active_flash_promotions()
    print("Active Promotions:", promotions)
    print("Active Flash Promotions:", flash_promotions)

# Schedule cleaning tasks (example with APScheduler)
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
scheduler.add_job(clean_expired_promotions, 'interval', minutes=10)
scheduler.add_job(clean_expired_flash_promotions, 'interval', minutes=10)
scheduler.start()
