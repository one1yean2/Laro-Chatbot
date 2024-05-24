from flask import Blueprint
from flask_redis import FlaskRedis
bp = Blueprint("promotion", __name__, url_prefix="/promotion")

@bp.route("/", methods=["GET", "POST"])
def create_promotion():
    
    
    return "promotion"


def create_flash_promotion():
    return "promotion"