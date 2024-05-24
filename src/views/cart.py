from flask import Blueprint

bp = Blueprint("cart", __name__, url_prefix="/cart")

@bp.route("/", methods=["GET", "POST"])
def create_Cart():
    return "cart"
